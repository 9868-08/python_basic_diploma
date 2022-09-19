from .photos_in_telegram import Photos
from utils.named_tuples import PhotoID


def get_photo_by_command(command: str) -> PhotoID:
    """Returns decorative photo id by called command"""

    if command == 'lowprice':
        return Photos.lowprice.value
    if command == 'highprice':
        return Photos.highprice.value
    if command == 'bestdeal':
        return Photos.bestdeal.value
