# LOKI Control Project - Application Template
Project to build the Linux OS image for generic target systems, with minimal configuration.

This repository is a prototype [LOKI](https://github.com/stfc-aeg/loki) project, a generic Embedded-Linux control
system that can be adapted to run application-specific control software based on the odin-control framework.

This template allows for the creation of an application repository with the following features:
- LOKI Core image build, including `odin-control` and dependencies
- Custom Application-specific Yocto layer (optional)
- Custom firmware (optional)

This project uses versions of LOKI v2.0.3+, and Xilinx toolchain 2023-2.

## Creating a Repository from this Template
#TODO

## Clone

Clone the repository (using a tag if necessary):

```bash
git clone git@github.com:stfc-aeg/loki-embedded-application-template.git
```
*Your repository will have a different name*

## Repository Setup


### Environment Setup

Load the Xilinx 2023-2 toolchain.
To do this as DSSG, run:

```bash
module load xilinx/2023-2
vivado_env
vitis_env
petalinux_env
```

The Makefile will check tool versions are correct as part of the build.

## Build 

### Create Firmware Project Only (for editing)

If you are just building the project, it is not necessary to run this step separately; it will simply save time by only creating the Vivado project for `loki-firmware` and then stopping.

```bash
make firmware-project
```

This will create the `loki-firmware/firmware/firmware.xpr` project file, which can be opened in Vivado.

### Whole Project

> BEFORE YOU RUN THIS, make sure you have used ssh agent to load keys used for github clones. It will fail without prompt for a password.

```bash
make
```

> [!NOTE]
> At this time, the FSBL / PMUFW is only being used as a prebuilt file, as the current LOKI 2023 toolchain is broken for Vitis.

On successive builds having modified only the control software, only the PetaLinux build should re-run.

The build files required for the board are in `./loki/os/petalinux-custom/images/linux/`:
- `image.ub` is the main Linux image. If there is an existing file, this can simply replace it to update the system
- `BOOT.BIN` is the customised U-Boot Bootloader, which is required but is unlikely to change unless the LOKI tag has been upated
- `boot.scr` is the U-Boot script, which is required but is unlikely to change unless the LOKI tag has been upated

