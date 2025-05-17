use std::process::Command;
use std::ffi::CString;
use std::os::raw::c_char;

/// Сжатие видео через FFmpeg из Python
#[no_mangle]
pub extern "C" fn compress_video(input_path: *const c_char, output_path: *const c_char) -> i32 {
    let input_cstr = unsafe { CString::from_raw(input_path as *mut c_char) };
    let output_cstr = unsafe { CString::from_raw(output_path as *mut c_char) };

    let input = input_cstr.to_str().unwrap_or("");
    let output = output_cstr.to_str().unwrap_or("");

    println!("Compressing: {} -> {}", input, output);

    let status = Command::new("ffmpeg")
        .args(&["-y", "-i", input, "-vcodec", "libx264", "-crf", "28", output])
        .status();

    match status {
        Ok(s) if s.success() => 0,
        _ => 1,
    }
}
