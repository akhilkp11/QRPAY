import frappe
import qrcode
import io
import base64

@frappe.whitelist()
def get_qr_code(data, scale=4):
    """
    Generate a base64 encoded QR code image from input data.
    Returns a data URI that can be used as img src.
    
    :param data: String to encode in QR code (e.g., UPI payment string)
    :param scale: Size factor (higher = larger QR code)
    """
    if not data:
        return ""
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=scale,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"