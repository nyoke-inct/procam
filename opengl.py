#!/usr/bin/env python3
'''
OpenGLでフルスクリーン表示してみるテスト 2021.12.24
参考サイト
https://qiita.com/a2kiti/items/39eba7616036fdd6fd36
http://codelabo.com/posts/20200228175104
https://qiita.com/Dhichisutto/items/76ec93c690caf20cedb9
https://www.alanshawn.com/tech/2019/06/10/pyopengl-1.html

needs:　環境を壊すかもしれんがanacondaからは直接インストールでけんかった
 conda update conda
 conda install pyopengl
 pip install PyOpenGL PyOpenGL_accelerate
 brew update
 brew upgrade
 brew install glfw3
 pip install glfw

 以下参考までに：
 パッケージのアップグレード
  softwareupdate --all --install --force 
'''

from OpenGL.GL import *
import glfw
import cv2

def main():
    # GLFW初期化
    if not glfw.init():
        return

    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    glfw.window_hint(glfw.RED_BITS, mode.bits.red)
    glfw.window_hint(glfw.GREEN_BITS, mode.bits.green)
    glfw.window_hint(glfw.BLUE_BITS, mode.bits.blue)
    glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)

    # ウィンドウを作成
    window = glfw.create_window(640, 480, 'Hello World', monitor, None)
    if not window:
        glfw.terminate()
        print('Failed to create window')
        return

    # コンテキストを作成します
    glfw.make_context_current(window)

    # OpenGLのバージョン等を表示します
    print('Vendor :', glGetString(GL_VENDOR))
    print('GPU :', glGetString(GL_RENDERER))
    print('OpenGL version :', glGetString(GL_VERSION))

    cv2.waitKey(50)

    # ウィンドウを破棄してGLFWを終了します
    glfw.destroy_window(window)
    glfw.terminate()


# Pythonのメイン関数はこんな感じで書きます
if __name__ == "__main__":
    main()


'''
def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not glfw.init():
            raise ValueError("Failed to initialize glfw")

        # Configure the OpenGL context
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, self.gl_version[0])
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, self.gl_version[1])
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.RESIZABLE, self.resizable)
        glfw.window_hint(glfw.DOUBLEBUFFER, True)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.SAMPLES, self.samples)

        monitor = None
        if self.fullscreen:
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)
            self._width, self._height = mode.size.width, mode.size.height

            glfw.window_hint(glfw.RED_BITS, mode.bits.red)
            glfw.window_hint(glfw.GREEN_BITS, mode.bits.green)
            glfw.window_hint(glfw.BLUE_BITS, mode.bits.blue)
            glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)

        self._window = glfw.create_window(self.width, self.height, self.title, monitor, None)
        self._has_focus = True

        if not self._window:
            glfw.terminate()
            raise ValueError("Failed to create window")

        self.cursor = self._cursor

        self._buffer_width, self._buffer_height = glfw.get_framebuffer_size(self._window)
        glfw.make_context_current(self._window)

        if self.vsync:
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

        glfw.set_key_callback(self._window, self.glfw_key_event_callback)
        glfw.set_cursor_pos_callback(self._window, self.glfw_mouse_event_callback)
        glfw.set_mouse_button_callback(self._window, self.glfw_mouse_button_callback)
        glfw.set_scroll_callback(self._window, self.glfw_mouse_scroll_callback)
        glfw.set_window_size_callback(self._window, self.glfw_window_resize_callback)
        glfw.set_char_callback(self._window, self.glfw_char_callback)
        glfw.set_window_focus_callback(self._window, self.glfw_window_focus)
        glfw.set_cursor_enter_callback(self._window, self.glfw_cursor_enter)
        glfw.set_window_iconify_callback(self._window, self.glfw_window_iconify)

        self.init_mgl_context()
        self.set_default_viewport() def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not glfw.init():
            raise ValueError("Failed to initialize glfw")

        # Configure the OpenGL context
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, self.gl_version[0])
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, self.gl_version[1])
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.RESIZABLE, self.resizable)
        glfw.window_hint(glfw.DOUBLEBUFFER, True)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.SAMPLES, self.samples)

        monitor = None
        if self.fullscreen:
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)
            self._width, self._height = mode.size.width, mode.size.height

            glfw.window_hint(glfw.RED_BITS, mode.bits.red)
            glfw.window_hint(glfw.GREEN_BITS, mode.bits.green)
            glfw.window_hint(glfw.BLUE_BITS, mode.bits.blue)
            glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)

        self._window = glfw.create_window(self.width, self.height, self.title, monitor, None)
        self._has_focus = True

        if not self._window:
            glfw.terminate()
            raise ValueError("Failed to create window")

        self.cursor = self._cursor

        self._buffer_width, self._buffer_height = glfw.get_framebuffer_size(self._window)
        glfw.make_context_current(self._window)

        if self.vsync:
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

        glfw.set_key_callback(self._window, self.glfw_key_event_callback)
        glfw.set_cursor_pos_callback(self._window, self.glfw_mouse_event_callback)
        glfw.set_mouse_button_callback(self._window, self.glfw_mouse_button_callback)
        glfw.set_scroll_callback(self._window, self.glfw_mouse_scroll_callback)
        glfw.set_window_size_callback(self._window, self.glfw_window_resize_callback)
        glfw.set_char_callback(self._window, self.glfw_char_callback)
        glfw.set_window_focus_callback(self._window, self.glfw_window_focus)
        glfw.set_cursor_enter_callback(self._window, self.glfw_cursor_enter)
        glfw.set_window_iconify_callback(self._window, self.glfw_window_iconify)

        self.init_mgl_context()
        self.set_default_viewport() 

'''