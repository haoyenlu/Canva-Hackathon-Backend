from diffusers import DiffusionPipeline
import torch



def inference_diffusion_model(prompt, num_images):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to(device)

    images = pipeline(prompt,num_images_per_prompt = num_images).images  # Return a list of PIL Image

    return images