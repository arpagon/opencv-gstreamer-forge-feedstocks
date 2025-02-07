#!/bin/bash -ex

mkdir -pm755 build
pushd build

export PKG_CONFIG_PATH="${PKG_CONFIG_PATH:+${PKG_CONFIG_PATH}:}${PREFIX}/lib/pkgconfig:${BUILD_PREFIX}/lib/pkgconfig"

EXTRA_FLAGS=""
if [ "${CONDA_BUILD_CROSS_COMPILATION}" = "1" ]; then
  # Use Meson cross-file flag to enable cross compilation
  EXTRA_FLAGS="--cross-file ${BUILD_PREFIX}/meson_cross_file.txt"
fi

export PKG_CONFIG="$(which pkg-config)"
# meson setup --buildtype=release --prefix="${PREFIX}" -Dlibdir="${PREFIX}/lib" -Dpython=enabled -Dgst-python:libpython-dir="${PREFIX}/lib" -Dgstreamer:ptp-helper-permissions=none -Dintrospection=enabled -Dorc=enabled -Dwebrtc=enabled -Dgst-plugins-bad:webrtcdsp=enabled -Drtsp_server=enabled -Dtls=enabled -Dlibnice=enabled -Dtools=enabled -Drs=enabled -Dgpl=enabled -Dbad=enabled -Dugly=enabled -Dlibav=enabled -Dgst-plugins-base:alsa=enabled -Dgst-plugins-base:gl=enabled -Dgst-plugins-base:opus=enabled -Dgst-plugins-good:pulse=enabled -Dgst-plugins-good:jack=enabled -Dgst-plugins-good:ximagesrc=enabled -Dgst-plugins-good:ximagesrc-xshm=enabled -Dgst-plugins-good:ximagesrc-xfixes=enabled -Dgst-plugins-good:ximagesrc-xdamage=enabled -Dgst-plugins-good:ximagesrc-navigation=enabled -Dgst-plugins-good:vpx=enabled -Dgst-plugins-bad:qsv=enabled -Dgst-plugins-bad:va=enabled -Dgst-plugins-bad:nvcodec=enabled -Dgst-plugins-good:v4l2=enabled -Dgst-plugins-bad:v4l2codecs=enabled -Dgst-plugins-bad:openh264=enabled -Dgst-plugins-ugly:x264=enabled -Dgst-plugins-bad:x265=enabled -Dgst-plugins-bad:aom=enabled -Dgst-plugins-bad:svtav1=enabled -Dgst-plugins-rs:rav1e=enabled -Dgst-plugins-rs:sodium=disabled -Dqt5=disabled -Dqt6=disabled -Ddoc=disabled -Ddevtools=disabled -Dexamples=disabled -Dgst-examples=disabled -Dnls=disabled -Dtests=disabled ${EXTRA_FLAGS} ..
meson setup --buildtype=release --prefix="${PREFIX}" \
    -Dlibdir="${PREFIX}/lib" \
    -Dpython=enabled \
    -Dgst-python:libpython-dir="${PREFIX}/lib" \
    -Dgstreamer:ptp-helper-permissions=none \
    -Dintrospection=enabled \
    -Dorc=enabled \
    -Dwebrtc=enabled \
    -Dgst-plugins-bad:webrtcdsp=enabled \
    -Drtsp_server=enabled \
    -Dtls=enabled \
    -Dlibnice=enabled \
    -Dtools=enabled \
    -Drs=enabled \
    -Dgpl=enabled \
    -Dbad=enabled \
    -Dugly=enabled \
    -Dlibav=enabled \
    -Dgst-plugins-base:alsa=enabled \
    -Dgst-plugins-base:gl=enabled \
    -Dgst-plugins-base:opus=enabled \
    -Dgst-plugins-good:pulse=enabled \
    -Dgst-plugins-good:jack=enabled \
    -Dgst-plugins-good:vpx=enabled \
    -Dgst-plugins-good:v4l2=enabled \
    -Dgst-plugins-bad:qsv=enabled \
    -Dgst-plugins-bad:va=enabled \
    -Dgst-plugins-bad:nvcodec=enabled \
    -Dgst-plugins-bad:v4l2codecs=enabled \
    -Dgst-plugins-bad:openh264=enabled \
    -Dgst-plugins-bad:x265=enabled \
    -Dgst-plugins-bad:aom=enabled \
    -Dgst-plugins-bad:svtav1=enabled \
    -Dgst-plugins-ugly:x264=enabled \
    -Dgst-plugins-rs:rav1e=enabled \
    -Dgst-plugins-rs:sodium=disabled \
    -Dqt5=disabled \
    -Dqt6=disabled \
    -Ddoc=disabled \
    -Ddevtools=disabled \
    -Dexamples=disabled \
    -Dgst-examples=disabled \
    -Dnls=disabled \
    -Dtests=disabled \
    ${EXTRA_FLAGS} ..

ninja
meson install

rm -rf "${PREFIX}/share/gdb"
rm -rf "${PREFIX}/share/gstreamer-1.0/gdb"

popd