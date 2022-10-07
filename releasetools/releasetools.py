#!/bin/env python3
#
# Copyright (C) 2020 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common
import re

def FullOTA_InstallEnd(info):
  OTA_InstallEnd(info)
  return

def IncrementalOTA_InstallEnd(info):
  info.input_zip = info.target_zip
  OTA_InstallEnd(info)
  return

def AddImage(info, basename, dest):
  name = basename
  data = info.input_zip.read("IMAGES/" + basename)
  common.ZipWriteStr(info.output_zip, name, data)
  info.script.Print("Patching {} image unconditionally...".format(dest.split('/')[-1]))
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))

def PrintInfo(info, dest):
  info.script.Print("Patching {} image unconditionally...".format(dest.split('/')[-1]))

def AddFirmwareImage(info, model, basename, dest, simple=False, offset=8):
  if ("RADIO/%s_%s" % (basename, model)) in info.input_zip.namelist():
    data = info.input_zip.read("RADIO/%s_%s" % (basename, model))
    common.ZipWriteStr(info.output_zip, "firmware/%s/%s" % (model, basename), data);
    info.script.Print("Patching {} image unconditionally...".format(basename.split('.')[0]));
    if simple:
      info.script.AppendExtra('package_extract_file("firmware/%s/%s", "%s");' % (model, basename, dest))
    else:
      uses_single_bota = dest == "/dev/block/by-name/bota"
      size = info.input_zip.getinfo("RADIO/%s_%s" % (basename, model)).file_size
      if not uses_single_bota:
        info.script.AppendExtra('assert(universal9830.mark_header_bt("%s", 0, 0, 0));' % dest);
      info.script.AppendExtra('assert(universal9830.write_data_bt("firmware/%s/%s", "%s", %d, %d));' % (model, basename, dest, offset, size))
      if not uses_single_bota:
        info.script.AppendExtra('assert(universal9830.mark_header_bt("%s", 0, 0, 3142939818));' % dest)
      return size
    return 0

def OTA_InstallEnd(info):
  PrintInfo(info, "/dev/block/by-name/dtbo")
  AddImage(info, "dtbo.img", "/dev/block/by-name/dtbo")
  PrintInfo(info, "/dev/block/by-name/vbmeta")
  AddImage(info, "vbmeta.img", "/dev/block/by-name/vbmeta")

  if "RADIO/models" in info.input_zip.namelist():
    modelsIncluded = []
    for model in info.input_zip.read("RADIO/models").decode('utf-8').splitlines():
      if "RADIO/version_%s" % model in info.input_zip.namelist():
        modelsIncluded.append(model)
        version = info.input_zip.read("RADIO/version_%s" % model).decode('utf-8').splitlines()[0]
        info.script.AppendExtra('# Firmware update to %s for %s' % (version, model))
        info.script.AppendExtra('ifelse (getprop("ro.boot.em.model") == "%s" &&' % model)
        info.script.AppendExtra('universal9830.verify_no_downgrade("%s") == "0" &&' % version)
        info.script.AppendExtra('getprop("ro.boot.bootloader") != "%s",' % version)
        offset = 8
        numImages = 0
        info.script.AppendExtra('assert(universal9830.mark_header_bt("/dev/block/by-name/bota", 0, 0, 0));')
        for image in 'harx.bin', 'keystorage.bin', 'ldfw.img', 'sboot.bin', 'ssp.img', 'tzar.img', 'tzsw.img ', 'uh.bin', 'up_param.bin':
          size = AddFirmwareImage(info, model, image, "/dev/block/by-name/bota", False, offset)
          if size > 0:
            numImages += 1
            offset += size + 36 # header size
        info.script.AppendExtra('assert(universal9830.mark_header_bt("/dev/block/by-name/bota", 0, %d, 3142939818));' % numImages)
        AddFirmwareImage(info, model, "modem.bin", "/dev/block/by-name/radio", True)
        AddFirmwareImage(info, model, "modem_debug.bin", "/dev/block/by-name/cp_debug", True)
        AddFirmwareImage(info, model, "dqmdbg.img", "/dev/block/by-name/dqmdbg", True)
        info.script.AppendExtra(',"");')

    modelCheck = ""
    for model in modelsIncluded:
      if len(modelCheck) > 0:
        modelCheck += ' || '
      modelCheck += 'getprop("ro.boot.em.model") == "%s"' % model
    if len(modelCheck) > 0:
      info.script.AppendExtra('%s || abort("Unsupported model, not updating firmware!");' % modelCheck)
  return

def FullOTA_InstallBegin(info):
  AddImage(info, "super_empty.img", "/dev/block/by-name/super")
  return
