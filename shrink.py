from PIL import Image

def shrink_image(input_path, output_path, width, height):
    # Open an image file
    with Image.open(input_path) as img:
        # Resize image
        resized_img = img.resize((width, height))
        
        # Save the resized image
        resized_img.save(output_path)
        print(f"Image saved as {output_path} with resolution {width}x{height}")

# Example usage
input_image_path = 'NumberNeuronal\\test\\onetest.jpg'  # Path to the original image
output_image_path = 'NumberNeuronal\\test\\shrinkonetest.jpg'  # Path to save the resized image
new_width = 48  # New width in pixels
new_height = 48  # New height in pixels

shrink_image(input_image_path, output_image_path, new_width, new_height)
