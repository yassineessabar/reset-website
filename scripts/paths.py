"""Shared paths for the build scripts. Every script resolves files from here, so the repo works from any checkout."""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
PUBLIC = REPO + 'public/'            # the deployable site
IMG = PUBLIC + 'assets/img/'         # images the pages use
CSS = PUBLIC + 'assets/css/'
CONTENT = REPO + 'scripts/content/'  # hand-written sections and captured layouts the pages are built from
DESIGN = REPO + 'design/'            # source material, never served
PHOTOS = DESIGN + 'photos/'          # full-size source photos (credits in design/CREDITS.md)
RENDERS = DESIGN + 'renders/'        # PNG/JPG intermediates the WebPs are made from
FONTS = DESIGN + 'fonts/'            # variable TTFs for rendering text into images
