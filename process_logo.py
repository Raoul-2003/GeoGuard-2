from PIL import Image
import numpy as np

def process_logo(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)
    
    r, g, b, a = data.T
    
    # White background threshold
    threshold = 200
    white_areas = (r > threshold) & (g > threshold) & (b > threshold)
    
    # Make background transparent
    data[..., 3][white_areas.T] = 0
    
    # Tint the non-white (logo) areas to a beautiful light blue 
    # matching the "secondary-fixed-dim" theme color (#adc6ff)
    non_white_areas = ~white_areas
    data[..., 0][non_white_areas.T] = 173 # R
    data[..., 1][non_white_areas.T] = 198 # G
    data[..., 2][non_white_areas.T] = 255 # B
    
    new_img = Image.fromarray(data)
    new_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
    new_img.save(output_path, "PNG")
    print(f"Saved processed logo to {output_path}")

if __name__ == "__main__":
    process_logo("logo.jpeg", "app/static/logo.png")
