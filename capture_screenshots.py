"""
Screenshot capture script for SpriteStack Studio README.
Launches the app, draws sample content, and captures screenshots of key features.
"""
import sys
import os
import random

# Ensure we can import app modules
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QColor, QImage, QPainter
from app.main_window import MainWindow

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "docs", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def draw_sample_pixel_art(window):
    """Draw a simple pixel art character on the canvas."""
    canvas = window.canvas
    
    # Set canvas to a good size
    if hasattr(canvas, 'current_image') and canvas.current_image:
        img = canvas.current_image
        
        # Draw a simple character (Mario-style silhouette)
        pixels = [
            # Hat (red)
            ((7, 2), (228, 59, 68)), ((8, 2), (228, 59, 68)), ((9, 2), (228, 59, 68)),
            ((6, 3), (228, 59, 68)), ((7, 3), (228, 59, 68)), ((8, 3), (228, 59, 68)),
            ((9, 3), (228, 59, 68)), ((10, 3), (228, 59, 68)),
            # Face (skin)
            ((7, 4), (232, 183, 150)), ((8, 4), (232, 183, 150)), ((9, 4), (232, 183, 150)),
            ((7, 5), (232, 183, 150)), ((8, 5), (232, 183, 150)), ((9, 5), (232, 183, 150)),
            # Eyes
            ((7, 4), (24, 20, 37)), ((9, 4), (24, 20, 37)),
            # Body (blue)
            ((7, 6), (18, 78, 137)), ((8, 6), (18, 78, 137)), ((9, 6), (18, 78, 137)),
            ((6, 7), (18, 78, 137)), ((7, 7), (18, 78, 137)), ((8, 7), (18, 78, 137)),
            ((9, 7), (18, 78, 137)), ((10, 7), (18, 78, 137)),
            ((7, 8), (18, 78, 137)), ((8, 8), (18, 78, 137)), ((9, 8), (18, 78, 137)),
            # Legs (brown)
            ((7, 9), (143, 86, 59)), ((9, 9), (143, 86, 59)),
            ((7, 10), (143, 86, 59)), ((9, 10), (143, 86, 59)),
        ]
        
        for (x, y), (r, g, b) in pixels:
            if 0 <= x < img.width() and 0 <= y < img.height():
                img.setPixelColor(x, y, QColor(r, g, b, 255))
        
        canvas.update()


def capture_screenshots(window):
    """Capture screenshots of the main window and key panels."""
    # Wait for the window to fully render
    window.showMaximized()
    QApplication.processEvents()
    
    # 1. Full window screenshot
    screen = QApplication.primaryScreen()
    if screen:
        pixmap = screen.grabWindow(window.winId())
        pixmap.save(os.path.join(SCREENSHOT_DIR, "studio_full.png"))
        print(f"Saved: studio_full.png ({pixmap.width()}x{pixmap.height()})")
    
    # 2. Just the canvas area
    if hasattr(window, 'canvas'):
        pixmap = window.canvas.grab()
        pixmap.save(os.path.join(SCREENSHOT_DIR, "canvas_editor.png"))
        print(f"Saved: canvas_editor.png")
    
    # 3. Tools panel
    if hasattr(window, 'tools_panel'):
        pixmap = window.tools_panel.grab()
        pixmap.save(os.path.join(SCREENSHOT_DIR, "tools_panel.png"))
        print(f"Saved: tools_panel.png")
    
    # 4. Layers panel
    if hasattr(window, 'layers_panel'):
        pixmap = window.layers_panel.grab()
        pixmap.save(os.path.join(SCREENSHOT_DIR, "layers_panel.png"))
        print(f"Saved: layers_panel.png")
    
    # 5. Timeline
    if hasattr(window, 'timeline'):
        pixmap = window.timeline.grab()
        pixmap.save(os.path.join(SCREENSHOT_DIR, "timeline.png"))
        print(f"Saved: timeline.png")
    
    # 6. 3D preview
    if hasattr(window, 'preview3d'):
        pixmap = window.preview3d.grab()
        pixmap.save(os.path.join(SCREENSHOT_DIR, "preview3d.png"))
        print(f"Saved: preview3d.png")
    
    # 7. Color palette
    if hasattr(window, 'palette_widget'):
        pixmap = window.palette_widget.grab()
        pixmap.save(os.path.join(SCREENSHOT_DIR, "palette.png"))
        print(f"Saved: palette.png")
    
    # 8. AI gen panel (if dockable)
    for attr in ['ai_gen_panel', 'ai_gen_dock', 'aiGenPanel']:
        if hasattr(window, attr):
            widget = getattr(window, attr)
            if hasattr(widget, 'show'):
                widget.show()
                QApplication.processEvents()
            pixmap = widget.grab()
            pixmap.save(os.path.join(SCREENSHOT_DIR, "ai_gen_panel.png"))
            print(f"Saved: ai_gen_panel.png")
            break
    
    # 9. AI chat panel
    for attr in ['ai_chat_panel', 'ai_chat_dock', 'aiChatPanel']:
        if hasattr(window, attr):
            widget = getattr(window, attr)
            if hasattr(widget, 'show'):
                widget.show()
                QApplication.processEvents()
            pixmap = widget.grab()
            pixmap.save(os.path.join(SCREENSHOT_DIR, "ai_chat_panel.png"))
            print(f"Saved: ai_chat_panel.png")
            break
    
    print(f"\nAll screenshots saved to: {SCREENSHOT_DIR}")
    print("Screenshots captured! Closing in 2s...")
    QTimer.singleShot(2000, QApplication.quit)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Draw sample content, then capture after a delay
    QTimer.singleShot(1500, lambda: draw_sample_pixel_art(window))
    QTimer.singleShot(3000, lambda: capture_screenshots(window))
    
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
