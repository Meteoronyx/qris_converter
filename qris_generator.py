import qrcode
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
STATIC_QRIS_DATA = os.getenv('STATIC_QRIS_DATA')
if not STATIC_QRIS_DATA:
    raise ValueError("Static QRIS data not found in environment variables. Please set STATIC_QRIS_DATA in .env file.")

def calculate_crc16(data: str) -> str:
    crc = 0xFFFF
    polynomial = 0x1021
    
    for char in data:
        crc ^= (ord(char) << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF
    
    return f"{crc:04X}"

def generate_dynamic_qris_data(amount: int) -> str:
    dynamic_data = STATIC_QRIS_DATA.replace("010211", "010212")
    
    amount_str = str(amount)
    length = len(amount_str)
    tag_54 = f"54{length:02d}{amount_str}"
    
    pos_53_end = dynamic_data.find("5303360") + 7
    dynamic_data = dynamic_data[:pos_53_end] + tag_54 + dynamic_data[pos_53_end:]
    
    crc_pos = dynamic_data.find("6304")
    data_to_checksum = dynamic_data[:crc_pos + 4]
    new_crc = calculate_crc16(data_to_checksum)
    dynamic_data = dynamic_data[:crc_pos + 4] + new_crc
    
    return dynamic_data

def _create_qr_code(dynamic_data: str) -> Image.Image:
    import logging
    logger = logging.getLogger(__name__)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(dynamic_data)
    qr.make(fit=True)
    logger.info("QR code object created.")
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    logger.info("QR code image created.")
    return qr_img

def _add_text_to_image(qr_img: Image.Image, amount: int) -> Image.Image:
    import logging
    logger = logging.getLogger(__name__)
    from PIL import ImageDraw, ImageFont
    
    qr_width, qr_height = qr_img.size
    new_height = qr_height + 50
    new_img = Image.new('RGB', (qr_width, new_height), color='white')
    logger.info("New image canvas created for QR code and text.")
    
    new_img.paste(qr_img, (0, 0))
    logger.info("QR code pasted onto new image.")
    
    draw = ImageDraw.Draw(new_img)
    try:
        font = ImageFont.truetype("arialbd.ttf", 35)
        logger.info("Arial font loaded successfully.")
    except IOError as e:
        logger.warning(f"Could not load Arial font: {e}")
        font = ImageFont.load_default()
        logger.info("Fallback to default font.")
    
    amount_text = f"Rp. {amount:,}"
    text_bbox = draw.textbbox((0, 0), amount_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (qr_width - text_width) // 2
    text_y = qr_height + 2
    draw.text((text_x, text_y), amount_text, font=font, fill='black')
    logger.info("Amount text drawn on image.")
    return new_img

def _save_image(img: Image.Image, amount: int) -> str:
    import logging
    logger = logging.getLogger(__name__)
    
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info("Output directory created.")
    else:
        logger.info("Output directory already exists.")
    
    output_path = os.path.join(output_dir, f"qris_{amount}.png")
    img.save(output_path)
    logger.info(f"Image saved to {output_path}.")
    return output_path

def generate_qris_qr(amount: int) -> str:
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        dynamic_data = generate_dynamic_qris_data(amount)
        logger.info("Dynamic QRIS data generated successfully.")
        
        qr_img = _create_qr_code(dynamic_data)
        final_img = _add_text_to_image(qr_img, amount)
        output_path = _save_image(final_img, amount)
        
        return output_path
    except Exception as e:
        logger.error(f"Error in generate_qris_qr: {e}", exc_info=True)
        raise
