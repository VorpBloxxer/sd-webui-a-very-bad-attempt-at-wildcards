import gradio as gr
from modules import sd_models, script_callbacks
import scripts.templater as templater 

singleton = templater.SingletonClass()

def ReloadModels():
    return gr.Dropdown.update(choices=sd_models.checkpoint_tiles())

def ReloadModelPlates(selected_model):
    templates = singleton.ModplatesNames(selected_model)
    return gr.Dropdown.update(choices=templates)

def LoadKeywords(model_name, template_name):
    template = singleton.loadModplates(model_name, template_name)
    
    if not template["global"]:
        template["global"] = ""
    
    return [gr.update(visible=True, value=template["global"]), gr.update(visible=True, value=template["start"]), gr.update(visible=True, value=template["end"])]

def SaveKeywords(model_name, template_name, keywordsDict):
    singleton.AddOrUpdModplate(model_name, template_name, keywordsDict)

def AddModelPlate(model_name, template_name):
    singleton.AddOrUpdModplate(model_name, template_name)
    return gr.Dropdown.update(value=template_name)

def AddKeywordPlate(template_name):
    print("Unfinished AddKeywordPlate")

def SaveModelPlateWrapper(model, template, global_text):
    SaveKeywords(model, template, {
        "global": global_text
    })
    
def SaveKeywordPlateWrapper(model, template, global_text):
    print("Unfinished SaveKeywordsPlateWrapper")

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as view:
        with gr.Accordion("ModelPlates"):
            with gr.Row():
                modelDropdown = gr.Dropdown(choices=sd_models.checkpoint_tiles(), label="Model")
                reloadModelBtn = gr.Button("Reload", scale=0)
                reloadModelBtn.click(ReloadModels, inputs=None, outputs=None)
                
            with gr.Row():
                modelPlateDropdown = gr.Dropdown(choices=[], label="ModelPlate")
                reloadTemplateBtn = gr.Button("Reload", scale=0)
                reloadTemplateBtn.click(ReloadModelPlates, inputs=modelDropdown, outputs=modelPlateDropdown)
                modelDropdown.change(ReloadModelPlates, inputs=modelDropdown, outputs=modelPlateDropdown)
                
            with gr.Row():
                modelPlateText = gr.Textbox(visible=True, label="Edit ModelPlate", lines=7)
            
            saveButton = gr.Button("Save")
            saveButton.click(
                SaveModelPlateWrapper, 
                inputs=[modelDropdown, modelPlateDropdown, modelPlateText], 
                outputs=None
            )
            
            with gr.Row():
                addModelPlateButton = gr.Button("Add Template to model", scale=0)
                newModelPlateName = gr.Textbox(visible=True, label="Add ModelPlate", lines=1)
                addModelPlateButton.click(AddModelPlate, inputs=[modelDropdown, newModelPlateName], outputs=modelPlateDropdown)
                
        with gr.Accordion("KeywordPlates"):
            keywordPlateDropdown = gr.Dropdown(choices=["ssss"], label="Select KeywordPlate")
            keywordsText = gr.Textbox(visible=True, label="Add Default Keywords", lines=7)
            saveButton = gr.Button("Save")
            saveButton.click(
                    SaveKeywordPlateWrapper, 
                    inputs=[keywordPlateDropdown, keywordsText], 
                    outputs=None
            )
            
            with gr.Row():
                addKeywordPlateButton = gr.Button("Add Template to model", scale=0)
                newKeywordPlateName = gr.Textbox(visible=True, label="Add KeywordPlate", lines=1)
                addKeywordPlateButton.click(AddKeywordPlate, inputs=[newKeywordPlateName], outputs=keywordPlateDropdown)
                
        return (
                (
                    view,
                    "Testing NullWildcards",
                    "Testing YamlLoader",
                ),
            )
        
script_callbacks.on_ui_tabs(on_ui_tabs)