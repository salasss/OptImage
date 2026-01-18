from PIL import Image
import io
def process_image(file_content: bytes,width: int = None,height: int = None,format:str = "WEBP",quality: int = 80)->io.BytesIO:
    """traitement of an image in bytes format, return a memoir buffer"""
    try:
        my_image = io.BytesIO(file_content)
        
        with Image.open(my_image)as img:
            if format.upper() in ["JPEG", "JPG"] and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
            if width or height:
                original_width, original_height = img.size
                if width and not height:
                    ratio=width/original_width
                    height = int(original_height*ratio)
                elif height and not width:
                    ratio= height/original_height
                    width = int(original_width*ratio)
                    
                    
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                
            output_buffer = io.BytesIO()
            save_format = format.upper() if format.upper() != "JPG" else "JPEG"
            
            img.save(output_buffer, format=save_format,quality=quality, optimize=True)
            
            output_buffer.seek(0)
            return output_buffer
    except Exception as e:
        raise ValueError(f"error:{str(e)}")
    