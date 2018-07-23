import glob
import struct

class Chunk(object):
    def __init__(self, fcc, data):
        self.fcc = bytearray()
        self.fcc.extend(fcc.encode())
        self.data = bytearray(data)

    def extend(self, data):
        self.data.extend(data)

    def to_bytes(self):
        return struct.pack("<4sL", self.fcc, len(self.data)) + self.data

class List(Chunk):
    def __init__(self, type, fcc, data):
        assert type in ["LIST", "RIFF"]

        super().__init__(fcc, data)
        self.fcc_type = bytearray()
        self.fcc_type.extend(type.encode())

    def to_bytes(self):
        return struct.pack("<4sL4s", self.fcc_type, len(self.data) + 4, self.fcc) + self.data

class MainAVIHeader(Chunk):
    dw_micros_per_frame = 0
    dw_max_bytes_per_sec = 0
    dw_padding_granularity = 0
    dw_flags = 0
    dw_total_frames = 0
    dw_initial_frames = 0
    dw_streams = 0
    dw_suggested_buffer_size = 0
    dw_width = 0
    dw_height = 0
    dw_reserved0 = 0
    dw_reserved1 = 0
    dw_reserved2 = 0
    dw_reserved3 = 0

    def __init__(self):
        super().__init__("avih", [])

    def to_bytes(self):
        self.data = struct.pack("<LLLLLLLLLLLLLL", self.dw_micros_per_frame, self.dw_max_bytes_per_sec,
                                self.dw_padding_granularity, self.dw_flags, self.dw_total_frames, self.dw_initial_frames,
                                self.dw_streams, self.dw_suggested_buffer_size, self.width, self.height,
                                self.dw_reserved0, self.dw_reserved1, self.dw_reserved2, self.dw_reserved3)
        return super().to_bytes()

class AVIStreamHeader(Chunk):
    fcc_type = bytearray()
    fcc_handler = bytearray()
    dw_flags = 0
    w_priority = 0
    w_language = 0
    dw_initial_frames = 0
    dw_scale = 0
    dw_rate = 0
    dw_start = 0
    dw_length = 0
    dw_suggested_buffer_size = 0
    dw_quality = 0
    dw_sample_size = 0
    rc_frame_left = 0
    rc_frame_top = 0
    rc_frame_right = 0
    rc_frame_bottom = 0

    def __init__(self):
        super().__init__("strh", [])

    def to_bytes(self):
        self.data = struct.pack("<4s4sLHHLLLLLLLLHHHH", self.fcc_type, self.fcc_handler, self.dw_flags,
                                self.w_priority, self.w_language, self.dw_initial_frames, self.dw_scale, self.dw_rate,
                                self.dw_start, self.dw_length, self.dw_suggested_buffer_size, self.dw_quality,
                                self.dw_sample_size, self.rc_frame_left, self.rc_frame_top, self.rc_frame_right,
                                self.rc_frame_bottom)
        return super().to_bytes()

class BitmapInfoHeader(Chunk):
    dw_size = 0
    l_width = 0
    l_height = 0
    w_planes = 0
    w_bit_count = 0
    dw_compression = 0
    dw_size_image = 0
    l_x_pels_per_meter = 0
    l_y_pels_per_meter = 0
    dw_clr_used = 0
    dw_clr_important = 0

    def __init__(self):
        super().__init__("strf", [])

    def to_bytes(self):
        self.data = struct.pack("<LllHHLLllLL", self.dw_size, self.l_width, self.l_height, self.w_planes,
                                self.w_bit_count, self.dw_compression, self.dw_size_image, self.l_x_pels_per_meter,
                                self.l_y_pels_per_meter, self.dw_clr_used, self.dw_clr_important)
        return super().to_bytes()


class MJPEGAVI(object):
    filename = "video.avi"
    avif = None
    frmf = None
    idxf = bytearray()
    width = 0
    height = 0
    total_frames = 0
    fps = 0

    def __init__(self, filename, fps):
        self.filename = filename
        self.fps = fps
        self.frmf = open(filename + ".temp", 'wb')

    def add_frame(self, frame_bytes):
        self.frmf.write(Chunk("00dc", frame_bytes).to_bytes())


        
    def _headers(self):
        self.avif.write(b"RIFF")
        self._write_len_field()
        self.avif.write(b"AVI ")
        self.avif.write(b"LIST")
        self._write_len_field()
        self.avif.write(b"hdrl")
        self.avif.write(b"avih")
        self.avif.write((0x38).to_bytes(4, "little"))
        self.avif.write((1000000 // self.fps).to_bytes(4, "little"))
        self.avif.write(INT32_ZERO) # Max Bytes per second
        self.avif.write(INT32_ZERO) # dwPaddingGranularity
        self.avif.write((0x10).to_bytes(4, "little")) # Flags

        self.frame_count_fields.append(self.avif.tell())
        self.avif.write(INT32_ZERO) # Number of frames

        self.avif.write(INT32_ZERO) # Initial frame for non-interleaved files
        self.avif.write(INT32_ONE) # Number of streams in video
        self.avif.write(INT32_ZERO) # dwSuggestedBufferSize
        self.avif.write(self.width.to_bytes(4, "little"))
        self.avif.write(self.height.to_bytes(4, "little"))
        self.avif.write(INT32_ZERO) # Reserved
        self.avif.write(INT32_ZERO)
        self.avif.write(INT32_ZERO)
        self.avif.write(INT32_ZERO)


        self.avif.write(b"LIST")
        self._write_len_field()
        self.avif.write(b"strl")
        self.avif.write(b"strh")
        self.avif.write((56).to_bytes(4, "little")) # Length of strh subchunk
        self.avif.write(b"vids")
        self.avif.write(b"mjpg")
        self.avif.write(INT32_ZERO) # dwFlags
        self.avif.write(INT32_ZERO) # wPriority, wLanguage
        self.avif.write(INT32_ZERO) # dwInitialFrames
        self.avif.write(INT32_ONE) # dwScale
        self.avif.write(self.fps.to_bytes(4, "little"))
        self.avif.write(INT32_ZERO) # usually zero

        self.frame_count_fields.append(self.avif.tell())
        self.avif.write(INT32_ZERO) # dwLength

        self.avif.write(INT32_ZERO) # dwSuggestedBufferSize
        self.avif.write(b"\xff\xff\xff\xff")  # dwQuality -1 for default
        self.avif.write(INT32_ZERO) # dwSampleSize, 0 means each frame is its own chunk
        self.avif.write(INT16_ZERO) # Rect
        self.avif.write(INT16_ZERO)
        self.avif.write(INT16_ZERO)
        self.avif.write(INT16_ZERO)

        self.avif.write(b"strf")
        self._write_len_field()
        self.avif.write((40).to_bytes(4, "little")) # biSize
        self.avif.write(self.width.to_bytes(4, "little"))
        self.avif.write(self.height.to_bytes(4, "little"))
        self.avif.write(INT16_ONE) # biPlanes, number of colour planes
        self.avif.write((24).to_bytes(2, "little")) # biBitCount, number of bits per pixel
        self.avif.write(b"MJPG")
        self.avif.write((self.width * self.height * 3).to_bytes(4, "little")) # biSizeImage, 0 for uncompressed data
        self.avif.write(INT32_ZERO) # biXPelsPerMetre
        self.avif.write(INT32_ZERO) # biYPelsPerMetre
        self.avif.write(INT32_ZERO) # biClrUsed, for 8bit only
        self.avif.write(INT32_ZERO) # biClrImportant
        self._finalise_len_field()
        self._finalise_len_field()
        self._finalise_len_field()

        self.avif.write(b"LIST")
        self._write_len_field()
        self.movi_pos = self.avif.tell()
        self.avif.write(b"movi")

    def _write_len_field(self):
        self.len_fields.append(self.avif.tell())
        self.avif.write(INT32_ZERO)

    def _finalise_len_field(self):
        pos = self.avif.tell()

        self.avif.seek(self.len_fields.pop(), 0)
        self.avif.write((pos - self.avif.tell() - 4).to_bytes(4, "little"))
        self.avif.seek(pos + 1 if pos & 0x01 else pos, 0)

    def add_frame(self, frame):
        if type(frame) != bytes:
            return

        pos = self.avif.tell()

        # TODO: check size

        self.avif.write(b"00dc")
        self._write_len_field()
        self.avif.write(frame)
        self._finalise_len_field()

        self.idxf.extend(b"00dc")
        self.idxf.extend((0x10).to_bytes(4, "little"))
        self.idxf.extend((pos - self.movi_pos).to_bytes(4, "little"))
        self.idxf.extend(len(frame).to_bytes(4, "little"))

        self.frames += 1

    def close(self):
        self._finalise_len_field()

        self.avif.write(b"idx1")
        self.avif.write(len(self.idxf).to_bytes(4, "little"))
        self.avif.write(self.idxf)

        for pos in self.frame_count_fields:
            self.avif.seek(pos, 0)
            self.avif.write(self.frames.to_bytes(4, "little"))

        self._finalise_len_field()

        self.avif.close()

def main():
    video = MJPEGAVI("video.avi", 64, 64, 60)

    for img in glob.iglob("./in/*.jpg"):
        with open(img, 'rb') as imf:
            video.add_frame(imf.read())

    video.close()


if __name__ == '__main__':
    main()