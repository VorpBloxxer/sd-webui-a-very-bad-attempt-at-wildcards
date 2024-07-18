import traceback, os, zipfile, shutil
import gradio as gr
from modules import images, script_callbacks, sd_models, scripts
from modules.processing import process_images, Processed
from modules.shared import opts, cmd_opts, state
from scripts.yamlLoaderV2 import *
import scripts.templater as templater
singleton = templater.SingletonClass()
currentP = None

def GetPrompt(prompts: list[str], prompt: str) -> str:
    return prompts[0] if prompts else prompt

def UpdateExtraParams(preloadPrompt,
                      originalPrompts):
    params = {"Globs prompt": preloadPrompt,
        "Original Prompts": originalPrompts}
    #currentP.extra_generation_params.update(params)

def ZipToWildcardsFolder(file):
    try:
        if file is not None and file.name.endswith('.zip'):
            wildcards_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wildcards")
            shutil.rmtree(wildcards_folder, ignore_errors=True)

            with zipfile.ZipFile(file.name, 'r') as zip_ref:
                zip_ref.extractall(wildcards_folder)
            print("Success: File processed and extracted successfully!")
            file
        else:
            print("Error: Please upload a valid .zip file.")
    except Exception as e:
        print(f"Error: {str(e)}")
    return gr.update(value=None)

def GetADetailerPrompts(scriptArgs):
    adetailerPrompts = {}
    for pos, element in enumerate(scriptArgs):
        if isinstance(element, dict) and 'ad_prompt' in element:
            adetailerPrompts.update({pos: element})
    return adetailerPrompts

def PrintInfo():
    print(f"Hr Fix: {getattr(currentP, 'enable_hr', False)}")
    print('\n\n\n\n\n\n\n')
    print('###################### vars(p) ###################')
    print(vars(currentP))
    print('\n\n\n\n\n\n\n')
    ## GETTING ADetailer prompts ##
    print('\n\n\n\n\n\n\n')
    print('###################### p.script_args_value ###################')
    print(currentP.script_args_value)
    print('\n\n\n\n\n\n\n')

def getPromptAndNegativePrompt(prompt, negativePrompt, originalNegatives, fileList):
    if negativePrompt is None or negativePrompt == "":
        negativePrompt = originalNegatives
    prompt, addedNegatives = cleanify(prompt, fileList, True)
    negativePrompt += ", " + addedNegatives
    negativePrompt = cleanify(negativePrompt, fileList)
    return prompt, negativePrompt
    
class GuiScript(scripts.Script):
    def __init__(self) -> None:
        super().__init__()
    def title(self):
        return "Null\'s Wildcards"
    def show(self, is_img2img):
            return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion('Null\'s Wildcards', open=False):
            with gr.Row():        
                dropfile = gr.File(
                    label="Upload .zip File"
                )
                dropfile.upload(ZipToWildcardsFolder, inputs=dropfile, outputs=dropfile)
                
                extensionEnabled = gr.Checkbox(
                    value=True,
                    label="Active"
                )
                
                printEnabled = gr.Checkbox(
                    value=False,
                    label="Print Prompts"
                )
                
                verbose = gr.Checkbox(
                    value=False,
                    label="Verbose"
                )
                
            with gr.Row():
                preloadPrompt = gr.Textbox(
                    lines=5,
                    max_lines=20,
                    placeholder="Input <wc:...> here",
                    label="Preload before prompts"
                )
        return [preloadPrompt, extensionEnabled, printEnabled, verbose]
    
    def process(self, p, preloadPrompt, extensionEnabled, printEnabled, verbose, *args):

        try:
            if not extensionEnabled:
                return
            global currentP
            currentP = p
            if printEnabled:
                PrintInfo()
            #setVerbose(verbose)
            
            hrFixEnabled = getattr(p, "enable_hr", False)
            originalPrompt = GetPrompt(p.all_prompts, p.prompt)
            originalHrPrompt = p.hr_prompt
            originalHrNegPrompt = p.hr_negative_prompt
            originalNegPrompt = GetPrompt(p.all_negative_prompts, p.negative_prompt)
            originalPreloadPrompt = preloadPrompt
            file_list = loadFiles()
            
            script_args_tuple = p.script_args_value
            script_args_list = list(script_args_tuple)
            
            for cur_count in range(p.n_iter):
                for cur_batch in range(p.batch_size):
                    index = p.batch_size * cur_count + cur_batch
                    flushGlobs()
                    _ = cleanify(singleton.currentKeywords, file_list)
                    _ = cleanify(singleton.currentModPlate, file_list)
                    preloadPrompt = cleanify(originalPreloadPrompt, file_list)
                    
                    
                    prompt, neg_prompt = getPromptAndNegativePrompt(originalPrompt, originalNegPrompt, originalNegPrompt, file_list)
                    
                    ad_prompts = GetADetailerPrompts(script_args_list)
                    for pos, ad_prompt in ad_prompts.items():
                        ad_prompt["ad_prompt"], ad_prompt["ad_negative_prompt"] = getPromptAndNegativePrompt(ad_prompt["ad_prompt"], ad_prompt["ad_negative_prompt"], originalNegPrompt, file_list)
                        script_args_list[pos]['ad_prompt'] =  ad_prompt["ad_prompt"]
                        script_args_list[pos]['ad_negative_prompt'] = ad_prompt["ad_negative_prompt"]
                          
                    p.all_prompts[index] = prompt
                    p.all_negative_prompts[index] = neg_prompt
                    
                    if hrFixEnabled:
                        hrprompt, neg_hrprompt = getPromptAndNegativePrompt(originalHrPrompt, originalHrNegPrompt, originalNegPrompt, file_list)
                        p.all_hr_prompts[index] = hrprompt
                        p.all_hr_negative_prompts[index] = neg_hrprompt
                        
            p.script_args_value = tuple(script_args_list)
            if printEnabled:
                print(p.all_prompts)
                print(p.all_negative_prompts)
                print(p.all_hr_prompts)
                print(p.all_hr_negative_prompts)
                for pos, ad_prompt in ad_prompts.items():
                    print(script_args_list[pos]['ad_prompt'])
                    print( script_args_list[pos]['ad_negative_prompt'])
            UpdateExtraParams(preloadPrompt, {originalPrompt, originalHrPrompt, originalPreloadPrompt})
            flushGlobs()
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
    def postprocess(self, *args):
        self.run_callback = False
        return

import scripts.templater as templater
script_callbacks.on_app_started(templater.PreloadFolders) 