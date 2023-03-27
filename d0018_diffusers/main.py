# encoding: utf-8

from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipeline.to("cuda")
img = pipeline("a bug catched by a man").images[0]
img.save('output.png')
