import os
from django.conf                                                    import settings

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)

    return name, ext

def upload_img_path(instance, filename):
    full_path       = settings.MEDIA_ROOT
    new_filename    = instance.code
    name, ext       = get_filename_ext(filename)
    finale_filename = f'{new_filename}{ext}'

    if os.path.exists(f"{full_path}/profiles"):
        os.chdir(f"{full_path}/profiles")
        for file in os.listdir("."):
            if os.path.isfile(file) and file.startswith(f"{finale_filename}"):
                try:
                    os.remove(file)
                except Exception as e:
                    pass

    return "profiles/{finale_filename}".format(new_filename=new_filename, finale_filename=finale_filename)
