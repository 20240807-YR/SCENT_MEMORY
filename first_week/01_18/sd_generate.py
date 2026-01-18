from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline
from prompt_builder import build_prompt, load_perfume_json
from demo_weather import get_weather, weather_to_visual_context

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "image"
IMAGE_DIR.mkdir(exist_ok=True)

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
).to("cpu")

data = load_perfume_json()
weather = get_weather()
weather_context = weather_to_visual_context(weather)

def generate(note):
    prompt = build_prompt(
        perfume_name=data["perfume"],
        note_type=note,
        note_data=data["notes"][note],
        weather_context=weather_context
    )
    image = pipe(prompt, num_inference_steps=20).images[0]
    image.save(IMAGE_DIR / f"{note}.png")

if __name__ == "__main__":
    generate("top")
    generate("middle")
    generate("base")