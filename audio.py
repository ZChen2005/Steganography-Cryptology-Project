import wave
import struct
import os


#Encoding Method
def audio_encoder(input_audio_path: str, output_audio_path: str, secret_message: str):

    #Open the WAV and read raw frames
    with wave.open(input_audio_path, 'rb') as wav_in:
        params     = wav_in.getparams()        # (nchannels, sampwidth, framerate, nframes, comptype, compname)
        raw_frames = wav_in.readframes(params.nframes)

    #Unpack frames into a list of integers
    nchannels, sampwidth, framerate, nframes, comptype, compname = params
    num_samples = nframes * nchannels
    if sampwidth == 1:
        fmt = f"{num_samples}B"       # unsigned 8-bit
    elif sampwidth == 2:
        fmt = f"<{num_samples}h"      # signed 16-bit little-endian
    else:
        raise ValueError("Only 8-bit or 16-bit PCM WAV supported")
    samples = list(struct.unpack(fmt, raw_frames))

    #Build the binary message + delimiter
    delimiter      = '10110110'  # marks end of message
    binary_message = ''.join(format(ord(c), '08b') for c in secret_message) + delimiter

    #Embed each bit into the LSB of successive samples
    if len(binary_message) > len(samples):
        raise ValueError("Message too long to encode in this audio file")
    for i, bit in enumerate(binary_message):
        samples[i] = (samples[i] & ~1) | int(bit)

    #Pack modified samples back to bytes
    modified_frames = struct.pack(fmt, *samples)

    #Write out new WAV with hidden data
    with wave.open(output_audio_path, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(modified_frames)

    print(f"Encoded {len(secret_message)} characters into {os.path.basename(output_audio_path)}")

#Decoding Method
def audio_decoder(stego_audio_path: str) -> str:

    # Read the stego WAV
    with wave.open(stego_audio_path, 'rb') as wav_in:
        params     = wav_in.getparams()
        raw_frames = wav_in.readframes(params.nframes)

    # 2) Unpack into integer samples
    nchannels, sampwidth, framerate, nframes, comptype, compname = params
    num_samples = nframes * nchannels
    if sampwidth == 1:
        fmt = f"{num_samples}B"
    elif sampwidth == 2:
        fmt = f"<{num_samples}h"
    else:
        raise ValueError("Only 8-bit or 16-bit PCM WAV supported")
    samples = struct.unpack(fmt, raw_frames)

    # 3) Extract LSBs
    bits = ''.join(str(sample & 1) for sample in samples)

    # 4) Reassemble bytes until the delimiter
    delimiter = '10110110'
    decoded_chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if byte == delimiter:
            break
        decoded_chars.append(chr(int(byte, 2)))

    message = ''.join(decoded_chars)
    print(f"Decoded message: {message}")
    return message


if __name__ == "__main__":

    #Encode
    audio_encoder(
        r"C:\Users\jonal\PycharmProjects\PythonProject5\audios\testAudonormal.wav",
        r"C:\Users\jonal\PycharmProjects\PythonProject5\audios\testAudonormalnew.wav",
        "The secret message is 42. https://www.amazon.com/Hitchhikers-Guide-Galaxy-Douglas-Adams/dp/0345418913/ref=sr_1_1?crid=25285HS4J4U8F&dib=eyJ2IjoiMSJ9.T9qfV-1KgRGkm_g-HFJrh8hxDdVja4HG7biiQCA7CDcwV7kLCWpJrdeplhse1nXMIOO6sSssJ01LPWp4uMuiTMEdtgUmE7I4LQGLzcM6l9jiQRcCwhRaqvutv-4ZPzgO7Tln0juAiCEo320ErwND8TZ2OD5JnZa2Kgc3XuXL60FNGYKDXeFGO7TqMjb00WNYXfJgv9qehGQ_31zgmYMrr1fzUZUpjytlD15qnVItq0A.3d7sSjnsCYRIQ92ZDvaAchfljrViDaG0-2NlhlhUuas&dib_tag=se&keywords=the+hitchhiker%27s+guide+to+the+galaxy&qid=1746763962&sprefix=the+hitc%2Caps%2C104&sr=8-1 "
    )

    # Decode
    recovered = audio_decoder(
        r"C:\Users\jonal\PycharmProjects\PythonProject5\audios\testAudonormalnew.wav"
    )
