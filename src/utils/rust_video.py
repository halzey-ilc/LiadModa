import ctypes
import os

# Путь к собранной библиотеке
LIB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../rust_video_engine/target/release/libvideoengine.dylib")
)
# Загружаем Rust-библиотеку
video_lib = ctypes.CDLL(LIB_PATH)

# Указываем типы аргументов
video_lib.compress_video.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
video_lib.compress_video.restype = ctypes.c_int

def compress_video(input_path: str, output_path: str) -> bool:
    input_bytes = input_path.encode("utf-8")
    output_bytes = output_path.encode("utf-8")

    result = video_lib.compress_video(input_bytes, output_bytes)
    return result == 0
