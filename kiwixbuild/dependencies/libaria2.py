from .base import (
    Dependency,
    ReleaseDownload,
    MakeBuilder
)

from kiwixbuild.utils import Remotefile, run_command

class Aria2(Dependency):
    name = "libaria2"

    class Source(ReleaseDownload):
        archive = Remotefile('libaria2-1.33.1.tar.gz',
                             '0616f11ef3ddd0c74be74ea2536be62ce168b99e3d6a35dea9d166b9cab9fbd1',
                             'https://github.com/aria2/aria2/archive/release-1.33.1.tar.gz')

        patches = ["libaria2_android.patch"]
        flatpak_no_autogen = True
        # Run it twice to pass `too many loops` error
        flatpak_command = "autoreconf -i; autoreconf -i"

        def _post_prepare_script(self, context):
            context.try_skip(self.extract_path)
            command = "autoreconf -i"
            run_command(command, self.extract_path, context)

    class Builder(MakeBuilder):
        configure_option = "--enable-libaria2 --disable-ssl --disable-bittorent --disable-metalink --without-sqlite3 --without-libxml2 --without-libexpat"
        @classmethod
        def get_dependencies(cls, platformInfo, allDeps):
            if (platformInfo.build == 'flatpak'):
                return []
            return ['zlib']