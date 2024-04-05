################################################################################
########                           Imports                              ########
################################################################################
import os, shutil, sys, platform, warnings
from typing import Optional
from invoke import Collection, Config, Exit, task
from shutil import which
from os import environ
from tabulate import tabulate
import pandas as pd
import glob
import re


################################################################################
########                      Root Directory Path                       ########
################################################################################
ROOT_DIR = os.path.dirname(__file__)
LOADER = "loader"
EXCAVATOR = "excavator"
CHEETAH = "cheetah"
TIPPER = "tipper"
DUMPER = "dumper"
GTRUCK = "gtruck"
BOOTLOADER = "bootloader"
LEGACY = "payload"
ALL = "all"
TOOLCHAIN_REPO_ENV = "TOOLCHAIN_REPO"
SUPPORTED_PROJECTS = [LOADER, EXCAVATOR, TIPPER, DUMPER, GTRUCK, BOOTLOADER]
SUPPORTED_PROJECTS_NICKNAME = [CHEETAH, LEGACY]


################################################################################
########                    Toolchain Executables                       ########
################################################################################
ARMGCC = "arm-none-eabi-gcc"
ARMSIZE = "arm-none-eabi-readelf"
ARMGDB = "arm-none-eabi-gdb"
ARMGDBPY = "arm-none-eabi-gdb-py"
ASTYLE = "astyle"
CPPCHECK = "cppcheck"
OPENOCD = "openocd"
DOXYGEN = "doxygen"
GRAPHVIZ = "dot"
PDFLATEX = "pdflatex"
HHC = "hhc"
STM32PROGRAMMERCLI = "STM32_Programmer_CLI"


################################################################################
########                    Toolchain Linux Directory                   ########
################################################################################
ARMGCC_LINUX = "gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux"
ASTYLE_LINUX = "astyle-linux"
CPPCHECK_LINUX = "cppcheck-linux"
OPENOCD_LINUX = "xpack-openocd-0.10.0-15-linux-x64"
DOXYGEN_LINUX = "doxygen-linux"
STM32PROGRAMMERCLI_LINUX = "stm32programmercli-linux"


################################################################################
########                    Toolchain Darwin Directory                  ########
################################################################################
ARMGCC_DARWIN = "gcc-arm-none-eabi-10-2020-q4-major-osx"
ASTYLE_DARWIN = "astyle-osx"
CPPCHECK_DARWIN = "cppcheck-osx"
OPENOCD_DARWIN = "xpack-openocd-0.10.0-15-darwin-x64"
DOXYGEN_DARWIN = "doxygen-osx"
STM32PROGRAMMERCLI_DARWIN = "stm32programmercli-osx"


################################################################################
########                    Toolchain Windows Directory                 ########
################################################################################
ARMGCC_WINDOWS = "gcc-arm-none-eabi-10-2020-q4-major-windows"
ASTYLE_WINDOWS = "astyle-windows"
CPPCHECK_WINDOWS = "cppcheck-windows"
OPENOCD_WINDOWS = "xpack-openocd-0.10.0-15-windows-x64"
DOXYGEN_WINDOWS = "doxygen-windows"
GRAPHVIZ_WINDOWS = "graphviz-windows"
PDFLATEX_WINDOWS = "miktex-windows"
HHC_WINDOWS = "hhc-windows"
STM32PROGRAMMERCLI_WINDOWS = "stm32programmercli-windows"


################################################################################
########                        Debug Constants                         ########
################################################################################
STLINK_GDB_PORT = 2331
OPENOCD_GDB_PORT = 2331
STLINK_TELNET_PORT = 19021
OPENOCD_TELNET_PORT = 109021

################################################################################
########                        Size Parameters                         ########
################################################################################
LOADER_RAM_START_ADDRESS = "0x20000000"
EXCAVATOR_RAM_START_ADDRESS = "0x20000000"
TIPPER_RAM_START_ADDRESS = "0x20000000"
DUMPER_RAM_START_ADDRESS = "0x20000000"
GTRUCK_RAM_START_ADDRESS = "0x20000000"
BOOTLOADER_RAM_START_ADDRESS = "0x20000000"

LOADER_RAM_END_ADDRESS = "0x20050000"
EXCAVATOR_RAM_END_ADDRESS = "0x20050000"
TIPPER_RAM_END_ADDRESS = "0x20050000"
DUMPER_RAM_END_ADDRESS = "0x20050000"
GTRUCK_RAM_END_ADDRESS = "0x20050000"
BOOTLOADER_RAM_END_ADDRESS = "0x20050000"

LOADER_FLASH_START_ADDRESS = "0x08040000"
EXCAVATOR_FLASH_START_ADDRESS = "0x08040000"
TIPPER_FLASH_START_ADDRESS = "0x08040000"
DUMPER_FLASH_START_ADDRESS = "0x08040000"
GTRUCK_FLASH_START_ADDRESS = "0x08040000"
BOOTLOADER_FLASH_START_ADDRESS = "0x08000000"

LOADER_FLASH_END_ADDRESS = "0x08100000"
EXCAVATOR_FLASH_END_ADDRESS = "0x08100000"
TIPPER_FLASH_END_ADDRESS = "0x08100000"
DUMPER_FLASH_END_ADDRESS = "0x08100000"
GTRUCK_FLASH_END_ADDRESS = "0x08100000"
BOOTLOADER_FLASH_END_ADDRESS = "0x08040000"

LOADER_QUADSPI_START_ADDRESS = "0x90000000"
EXCAVATOR_QUADSPI_START_ADDRESS = "0x90000000"
TIPPER_QUADSPI_START_ADDRESS = "0x90000000"
DUMPER_QUADSPI_START_ADDRESS = "0x90000000"
GTRUCK_QUADSPI_START_ADDRESS = "0x90000000"
BOOTLOADER_QUADSPI_START_ADDRESS = "0x90000000"

LOADER_QUADSPI_END_ADDRESS = "0x91000000"
EXCAVATOR_QUADSPI_END_ADDRESS = "0x91000000"
TIPPER_QUADSPI_END_ADDRESS = "0x91000000"
DUMPER_QUADSPI_END_ADDRESS = "0x91000000"
GTRUCK_QUADSPI_END_ADDRESS = "0x91000000"
BOOTLOADER_QUADSPI_END_ADDRESS = "0x91000000"

LOADER_SDRAM_START_ADDRESS = "0x600BB804"
EXCAVATOR_SDRAM_START_ADDRESS = "0x600BB804"
TIPPER_SDRAM_START_ADDRESS = "0x600BB804"
DUMPER_SDRAM_START_ADDRESS = "0x600BB804"
GTRUCK_SDRAM_START_ADDRESS = "0x600BB804"
BOOTLOADER_SDRAM_START_ADDRESS = "0x600BB804"

LOADER_SDRAM_END_ADDRESS = "0x61000000"
EXCAVATOR_SDRAM_END_ADDRESS = "0x61000000"
TIPPER_SDRAM_END_ADDRESS = "0x61000000"
DUMPER_SDRAM_END_ADDRESS = "0x61000000"
GTRUCK_SDRAM_END_ADDRESS = "0x61000000"
BOOTLOADER_SDRAM_END_ADDRESS = "0x61000000"

RAM = 0
FLASH = 1
QUADSPI = 2
SDRAM = 3

################################################################################
########                       flash Parameters                         ########
################################################################################
SWD_FREQUENCY = 4000000

LOADER_QSPI_START_ADDRESS = "0x90000000"
EXCAVATOR_QSPI_START_ADDRESS = "0x90000000"
TIPPER_QSPI_START_ADDRESS = "0x90000000"
DUMPER_QSPI_START_ADDRESS = "0x90000000"
GTRUCK_QSPI_START_ADDRESS = "0x90000000"
BOOTLOADER_QSPI_START_ADDRESS = "0x90000000"

LOADER_APP_START_ADDRESS = "0x08040000"
EXCAVATOR_APP_START_ADDRESS = "0x08040000"
TIPPER_APP_START_ADDRESS = "0x08040000"
DUMPER_APP_START_ADDRESS = "0x08040000"
GTRUCK_APP_START_ADDRESS = "0x08040000"
BOOTLOADER_APP_START_ADDRESS = "0x08000000"


################################################################################
########                            Jenkins                             ########
################################################################################
JENKINS_BUILD_STAGE = "BUILD"
JENKINS_BEAUTIFY_STAGE = "BEAUTIFY"
JENKINS_LINT_STAGE = "LINT"
JENKINS_TEST_STAGE = "TEST"
JENKINS_BUILD_STAGES = [JENKINS_BUILD_STAGE, JENKINS_BEAUTIFY_STAGE, JENKINS_LINT_STAGE, JENKINS_TEST_STAGE]


def check_exe(exe, download_url):
    exe_path = which(exe)
    if not exe_path:
        msg = (
            "Couldn't find `{}`."
            "This tool can be found here:"
            "> {}.".format(exe, download_url)
        )
        warnings.warn(msg)


def check_arm_toolchain():
    """Run as a `pre` task to check for the presence of the ARM toolchains"""
    armgcc_url = "https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads"
    check_exe(ARMGCC, armgcc_url)
    check_exe(ARMSIZE, armgcc_url)
    check_exe(ARMGDB, armgcc_url)


def check_beautify_toolchain():
    """Run as a `pre` task to check for the presence of the ARM toolchain"""
    beautify_url = "http://astyle.sourceforge.net"
    check_exe(ASTYLE, beautify_url)


def check_lint_toolchain():
    """Run as a `pre` task to check for the presence of the ARM toolchain"""
    lint_url = "http://cppcheck.sourceforge.net"
    check_exe(CPPCHECK, lint_url)


def check_openocd_toolchain():
    """Run as a `pre` task to check for the presence of the ARM toolchain"""
    openocd_url = "http://openocd.org/getting-openocd"
    check_exe(OPENOCD, openocd_url)

    
def check_doxygen_toolchain():
    """Run as a `pre` task to check for the presence of the doxygen toolchain"""
    doxygen_url = "https://www.doxygen.nl/download.html"
    check_exe(DOXYGEN, doxygen_url)


def check_graphviz_toolchain():
    """Run as a `pre` task to check for the presence of the graphviz toolchain"""
    graphviz_url = "https://graphviz.org/download/"
    check_exe(GRAPHVIZ, graphviz_url)
    
    
def check_miktex_toolchain():
    """Run as a `pre` task to check for the presence of the miketex toolchain"""
    miktex_url = "https://miktex.org/download"
    check_exe(PDFLATEX, miktex_url)


def check_hhc_toolchain():
    """Run as a `pre` task to check for the presence of the miketex toolchain"""
    hhc_url = "https://www.helpndoc.com/step-by-step-guides/how-to-download-and-install-microsofts-html-help-workshop-compiler/"
    check_exe(HHC, hhc_url)
    

def check_stm32programmercli_toolchain():
    """Run as a `pre` task to check for the presence of the stm32cube programmer toolchain"""
    stm32programmercli_url = "https://www.st.com/en/development-tools/stm32cubeprog.html"
    check_exe(STM32PROGRAMMERCLI, stm32programmercli_url)

    
def check_toolchain():
    check_arm_toolchain()
    check_beautify_toolchain()
    check_lint_toolchain()
    check_openocd_toolchain()
    check_doxygen_toolchain()
    check_graphviz_toolchain()
    check_miktex_toolchain()
    check_hhc_toolchain()
    check_stm32programmercli_toolchain()


def check_cheetah_project():
    global ARMGCC, ARMSIZE, ARMGDB, ARMGDBPY, ASTYLE, CPPCHECK, OPENOCD, DOXYGEN, STM32PROGRAMMERCLI, GRAPHVIZ, PDFLATEX, HHC
    if TOOLCHAIN_REPO_ENV in os.environ:
        print("Using toolchains available from EMBSW-TOOLCHAIN repo")
        BIN = "bin"
        TOOLCHAIN_REPO = os.environ['TOOLCHAIN_REPO']
        ARMGCC_DIR = os.path.join(TOOLCHAIN_REPO, "embsw-toolchain-armgcc")
        ASTYLE_DIR = os.path.join(TOOLCHAIN_REPO, "embsw-toolchain-astyle")
        CPPCHECK_DIR = os.path.join(TOOLCHAIN_REPO, "embsw-toolchain-cppcheck")
        OPENOCD_DIR = os.path.join(TOOLCHAIN_REPO, "embsw-toolchain-openocd")
        DOXYGEN_DIR = os.path.join(TOOLCHAIN_REPO, "embsw-toolchain-doxygen")
        STM32PROGRAMMERCLI_DIR = os.path.join(TOOLCHAIN_REPO, "embsw-toolchain-stm32programmercli")
        if platform.system() == "Linux":
            ARMGCC = os.path.join(ARMGCC_DIR, ARMGCC_LINUX, BIN, ARMGCC)
            ARMSIZE = os.path.join(ARMGCC_DIR, ARMGCC_LINUX, BIN, ARMSIZE)
            ARMGDB = os.path.join(ARMGCC_DIR, ARMGCC_LINUX, BIN, ARMGDB)
            ARMGDBPY = os.path.join(ARMGCC_DIR, ARMGCC_LINUX, BIN, ARMGDBPY)
            ASTYLE = os.path.join(ASTYLE_DIR, ASTYLE_LINUX, BIN, ASTYLE)
            CPPCHECK = os.path.join(CPPCHECK_DIR, CPPCHECK_LINUX, BIN, CPPCHECK)
            OPENOCD = os.path.join(OPENOCD_DIR, OPENOCD_LINUX, BIN, OPENOCD)
            DOXYGEN = os.path.join(DOXYGEN_DIR, DOXYGEN_LINUX, BIN, DOXYGEN)
            STM32PROGRAMMERCLI = os.path.join(STM32PROGRAMMERCLI_DIR, STM32PROGRAMMERCLI_LINUX, BIN, STM32PROGRAMMERCLI)
        elif platform.system() == "Darwin":
            ARMGCC = os.path.join(ARMGCC_DIR, ARMGCC_DARWIN, BIN, ARMGCC)
            ARMSIZE = os.path.join(ARMGCC_DIR, ARMGCC_DARWIN, BIN, ARMSIZE)
            ARMGDB = os.path.join(ARMGCC_DIR, ARMGCC_DARWIN, BIN, ARMGDB)
            ARMGDBPY = os.path.join(ARMGCC_DIR, ARMGCC_DARWIN, BIN, ARMGDBPY)
            ASTYLE = os.path.join(ASTYLE_DIR, ASTYLE_DARWIN, BIN, ASTYLE)
            CPPCHECK = os.path.join(CPPCHECK_DIR, CPPCHECK_DARWIN, BIN, CPPCHECK)
            OPENOCD = os.path.join(OPENOCD_DIR, OPENOCD_DARWIN, BIN, OPENOCD)
            DOXYGEN = os.path.join(DOXYGEN_DIR, DOXYGEN_DARWIN, BIN, DOXYGEN)
            STM32PROGRAMMERCLI = os.path.join(STM32PROGRAMMERCLI_DIR, STM32PROGRAMMERCLI_DARWIN, BIN, STM32PROGRAMMERCLI)
        elif platform.system() == "Windows":
            ARMGCC = os.path.join(ARMGCC_DIR, ARMGCC_WINDOWS, BIN, ARMGCC)
            ARMSIZE = os.path.join(ARMGCC_DIR, ARMGCC_WINDOWS, BIN, ARMSIZE)
            ARMGDB = os.path.join(ARMGCC_DIR, ARMGCC_WINDOWS, BIN, ARMGDB)
            ARMGDBPY = os.path.join(ARMGCC_DIR, ARMGCC_WINDOWS, BIN, ARMGDBPY)
            ASTYLE = os.path.join(ASTYLE_DIR, ASTYLE_WINDOWS, BIN, ASTYLE)
            CPPCHECK = os.path.join(CPPCHECK_DIR, CPPCHECK_WINDOWS, BIN, CPPCHECK)
            OPENOCD = os.path.join(OPENOCD_DIR, OPENOCD_WINDOWS, BIN, OPENOCD)
            DOXYGEN = os.path.join(DOXYGEN_DIR, DOXYGEN_WINDOWS, BIN, DOXYGEN)
            GRAPHVIZ = os.path.join(DOXYGEN_DIR, GRAPHVIZ_WINDOWS, BIN, GRAPHVIZ)
            PDFLATEX = os.path.join(DOXYGEN_DIR, PDFLATEX_WINDOWS, BIN, PDFLATEX)
            HHC = os.path.join(DOXYGEN_DIR, HHC_WINDOWS, BIN, HHC)
            STM32PROGRAMMERCLI = os.path.join(STM32PROGRAMMERCLI_DIR, STM32PROGRAMMERCLI_WINDOWS, BIN, STM32PROGRAMMERCLI)
        else:
            msg = ("Unsupported platform !!! You are different from the crowd")
            raise Exit(msg)
    else:
        print("Hopefully you have added following toolchains to your PATH environment variable")
        check_toolchain()

def check_legacy_project():
    pass


def check_project(project=None):
    project = project.lower()
    if project is None:
        msg = (
            "Please mention the project to build.\n"
            "List of supported projects: {}\n\n"
            .format(SUPPORTED_PROJECTS)
        )
        raise Exit(msg)
    if project not in SUPPORTED_PROJECTS and project != ALL:
        msg = (
            "Please mention a supported project.\n"
            "List of supported projects: {}\n\n"
            .format(SUPPORTED_PROJECTS)
        )
        raise Exit(msg)

    if CHEETAH in project:
        check_cheetah_project()
    elif LEGACY in project:
        check_legacy_project()
    else:
        check_cheetah_project()
        check_legacy_project()


def run_make(ctx, project, parallel=False, thread=8):
    if parallel:
        if thread > 1:
            cmd = f'make -j{thread} {project}'
            ctx.run(cmd)
        else:
            print("Please specify more than 1 thread for parallel builds")
    else:
        cmd = f'make -j{thread} {project}'
        ctx.run(cmd)


def run_clean(ctx):
    ctx.run("make clean")
        

def run_size(ctx, project):
    # Fetch the end address from each section
    if project == LOADER:
        ram_start_address = LOADER_RAM_START_ADDRESS
        flash_start_address = LOADER_FLASH_START_ADDRESS
        quadspi_start_address = LOADER_QUADSPI_START_ADDRESS
        sdram_start_address = LOADER_SDRAM_START_ADDRESS
        ram_end_address = LOADER_RAM_END_ADDRESS
        flash_end_address = LOADER_FLASH_END_ADDRESS
        quadspi_end_address = LOADER_QUADSPI_END_ADDRESS
        sdram_end_address = LOADER_SDRAM_END_ADDRESS
    elif project == EXCAVATOR:
        ram_start_address = EXCAVATOR_RAM_START_ADDRESS
        flash_start_address = EXCAVATOR_FLASH_START_ADDRESS
        quadspi_start_address = EXCAVATOR_QUADSPI_START_ADDRESS
        sdram_start_address = EXCAVATOR_SDRAM_START_ADDRESS
        ram_end_address = EXCAVATOR_RAM_END_ADDRESS
        flash_end_address = EXCAVATOR_FLASH_END_ADDRESS
        quadspi_end_address = EXCAVATOR_QUADSPI_END_ADDRESS
        sdram_end_address = EXCAVATOR_SDRAM_END_ADDRESS
    elif project == TIPPER:
        ram_start_address = TIPPER_RAM_START_ADDRESS
        flash_start_address = TIPPER_FLASH_START_ADDRESS
        quadspi_start_address = TIPPER_QUADSPI_START_ADDRESS
        sdram_start_address = TIPPER_SDRAM_START_ADDRESS
        ram_end_address = TIPPER_RAM_END_ADDRESS
        flash_end_address = TIPPER_FLASH_END_ADDRESS
        quadspi_end_address = TIPPER_QUADSPI_END_ADDRESS
        sdram_end_address = TIPPER_SDRAM_END_ADDRESS
    elif project == DUMPER:
        ram_start_address = DUMPER_RAM_START_ADDRESS
        flash_start_address = DUMPER_FLASH_START_ADDRESS
        quadspi_start_address = DUMPER_QUADSPI_START_ADDRESS
        sdram_start_address = DUMPER_SDRAM_START_ADDRESS
        ram_end_address = DUMPER_RAM_END_ADDRESS
        flash_end_address = DUMPER_FLASH_END_ADDRESS
        quadspi_end_address = DUMPER_QUADSPI_END_ADDRESS
        sdram_end_address = DUMPER_SDRAM_END_ADDRESS
    elif project == GTRUCK:
        ram_start_address = GTRUCK_RAM_START_ADDRESS
        flash_start_address = GTRUCK_FLASH_START_ADDRESS
        quadspi_start_address = GTRUCK_QUADSPI_START_ADDRESS
        sdram_start_address = GTRUCK_SDRAM_START_ADDRESS
        ram_end_address = GTRUCK_RAM_END_ADDRESS
        flash_end_address = GTRUCK_FLASH_END_ADDRESS
        quadspi_end_address = GTRUCK_QUADSPI_END_ADDRESS
        sdram_end_address = GTRUCK_SDRAM_END_ADDRESS
    elif project == BOOTLOADER:
        ram_start_address = BOOTLOADER_RAM_START_ADDRESS
        flash_start_address = BOOTLOADER_FLASH_START_ADDRESS
        quadspi_start_address = BOOTLOADER_QUADSPI_START_ADDRESS
        sdram_start_address = BOOTLOADER_SDRAM_START_ADDRESS
        ram_end_address = BOOTLOADER_RAM_END_ADDRESS
        flash_end_address = BOOTLOADER_FLASH_END_ADDRESS
        quadspi_end_address = BOOTLOADER_QUADSPI_END_ADDRESS
        sdram_end_address = BOOTLOADER_SDRAM_END_ADDRESS
    
    # ELF file check 
    project_path = "build/" + project + "/" + project + ".elf"
    try:
        f = open(project_path, 'r')
    except IOError:
        print('\nELF file not found : '+ project +'\n')
        return
    
    # Find FLASH & RAM size
    cmd = f'{ARMSIZE} -l {project_path}' 
    output = ctx.run(cmd, hide= 'out') #hide= 'out' used to hide the stdout data in invoke frame work
    
    print("")
    a_string = str(output)
    section_data = re.findall(r'0x[0-9A-F]+', a_string, re.I)

    ram_used = find_memory_usage(ram_start_address, section_data, RAM)
    ram_max_size = int(ram_end_address,16) - int(ram_start_address,16)
    ram_free = ram_max_size - ram_used
    ram_usage = percentage_calculation(ram_used, ram_max_size)

    flash_used = find_memory_usage(flash_start_address, section_data, FLASH)
    flash_max_size = int(flash_end_address,16) - int(flash_start_address,16)
    flash_free = flash_max_size - flash_used
    flash_usage = percentage_calculation(flash_used, flash_max_size)

    quadspi_used = find_memory_usage(quadspi_start_address, section_data, QUADSPI)
    # check quadspi section in elf file
    if quadspi_used != None:  
        quadspi_max_size = int(quadspi_end_address,16) - int(quadspi_start_address,16)
        quadspi_free = quadspi_max_size - quadspi_used
        quadspi_usage = percentage_calculation(quadspi_used, quadspi_max_size)

    sdram_used = find_memory_usage(sdram_start_address, section_data, SDRAM)
     # check sdram section in elf file
    if sdram_used != None:
        sdram_max_size = int(sdram_end_address,16) - int(sdram_start_address,16)
        sdram_free = sdram_max_size - sdram_used
        sdram_usage = percentage_calculation(sdram_used, sdram_max_size)
    
    table = {'Region':['RAM', 'FLASH', 'QUADSPI', 'SDRAM'],
        'Start address':[ram_start_address, flash_start_address, quadspi_start_address, sdram_start_address],
        'End address':[ram_end_address, flash_end_address, quadspi_end_address, sdram_end_address],
        'Size':[str(ram_max_size), str(flash_max_size), str(quadspi_max_size), str(sdram_max_size)],
        'Free':[str(ram_free), str(flash_free), str(quadspi_free), str(sdram_free)],
        'Used':[str(ram_used), str(flash_used), str(quadspi_used), str(sdram_used)],
        'Usage':[str(ram_usage), str(flash_usage), str(quadspi_usage), str(sdram_usage)]
        }
    tableframe = pd.DataFrame(table)

    if quadspi_used is None and sdram_used is None:
        tableframe = tableframe.drop(tableframe.index[[2, 3]])
    elif quadspi_used is None:
        tableframe = tableframe.drop(tableframe.index[[2]])
    elif sdram_used is None:
        tableframe = tableframe.drop(tableframe.index[[3]])

    print(tabulate(tableframe, headers='keys', tablefmt='fancy_grid', showindex=False))


def run_doxygen(ctx, project):
    #set doxyfile path
    doxyfile_path = project + "/Doxygen/Doxyfile"
    
    #checky doxyfile 
    try:
        f = open(doxyfile_path, 'r')
    except IOError:
        print('Doxyfile not found : '+ project)
        print("")
        return
  
    #run doxyfile
    cmd = f'{DOXYGEN} {doxyfile_path}' 
    ctx.run(cmd) 
    
    #make chm file path
    chm_file_path = project + "/Doxygen/html"
    
    #make chm file
    with ctx.cd(chm_file_path):
        ctx.run(f'{HHC} index.hhp')
    
    #remove unwanted files in latex folder
    chm_file_path = project + "/Doxygen/html/*.*" 
    for CleanUp in glob.glob(chm_file_path):
        if not CleanUp.endswith('index.chm'):    
            os.remove(CleanUp)  
            
    #set tex path
    pdf_file_path = project + "/Doxygen/latex"
    
    #make pdf file
    with ctx.cd(pdf_file_path):
        ctx.run(f'{PDFLATEX} refman.tex')
    
    #remove unwanted files in latex folder
    pdf_file_path = project + "/Doxygen/latex/*.*" 
    for CleanUp in glob.glob(pdf_file_path):
        if not CleanUp.endswith('refman.pdf'):    
            os.remove(CleanUp)
    
    #remove makefile in latex project
    pdf_file_path = project + "/Doxygen/latex/Makefile"
    os.remove(pdf_file_path) 
    
    move_and_rename_doxygen_files(project=project, folder_name="html", file_name="index", file_format=".chm")
    move_and_rename_doxygen_files(project=project, folder_name="latex", file_name="refman", file_format=".pdf")

  
def run_astyle(ctx, project, check=False):
    if check:
        if project != BOOTLOADER:
            cmd = f'{ASTYLE} --options=astyle_c.options.txt --recursive --dry-run --errors-to-stdout LCSApp/{project}/*.c,*.h'
        elif project == BOOTLOADER:
            cmd = f'{ASTYLE} --options=astyle_c.options.txt --recursive --dry-run --errors-to-stdout LCSBoot/*.c,*.h'
    else:
        if project != BOOTLOADER:
            cmd = f'{ASTYLE} --options=astyle_c.options.txt --recursive --formatted LCSApp/{project}/*.c,*.h'
        elif project == BOOTLOADER:
            cmd = f'{ASTYLE} --options=astyle_c.options.txt --recursive --formatted LCSBoot/*.c,*.h'
    ctx.run(cmd)


def run_cppcheck(ctx, project):
    if project == LOADER or project == EXCAVATOR:
        cmd = f'{CPPCHECK} --force LCSApp/{project}/' #--addon=misra.py
    elif project == BOOTLOADER:
        cmd = f'{CPPCHECK} --force LCSBoot/' #--addon=misra.py
    ctx.run(cmd)


def run_flash(ctx, project, interface="swd", config=None, exl=False):
    #if configuration selected as usb
    if interface == "usb":
        if config is None:
            print("Error : Config usb port number")
            return
        command = "-c port=usb" + str(config)
    else:
        if config is None:
            config = SWD_FREQUENCY
        command = "-c port=swd" + " freq=" + str(config) + " ap=0"

    elf_file_path = "build/" + project + "/" + project + ".elf"

    #checky bin file 
    try:
        f = open(elf_file_path, 'r')
    except IOError:
        print('elf file not found : '+ project)
        print("")
        return

    if exl:
        # Fetch external loader address
        if project == LOADER:
            EXTERNAL_LOADER_ADDRESS = LOADER_QSPI_START_ADDRESS
        elif project == EXCAVATOR:
            EXTERNAL_LOADER_ADDRESS = EXCAVATOR_QSPI_START_ADDRESS
        elif project == TIPPER:
            EXTERNAL_LOADER_ADDRESS = TIPPER_QSPI_START_ADDRESS
        elif project == DUMPER:
            EXTERNAL_LOADER_ADDRESS = DUMPER_QSPI_START_ADDRESS
        elif project == GTRUCK:
            EXTERNAL_LOADER_ADDRESS = GTRUCK_QSPI_START_ADDRESS
        elif project == BOOTLOADER:
            EXTERNAL_LOADER_ADDRESS = BOOTLOADER_QSPI_START_ADDRESS

        external_command = EXTERNAL_LOADER_ADDRESS + " -el STM32F746.stldr"
        cmd = f'{STM32PROGRAMMERCLI} {command} -w {elf_file_path} {external_command}'
    else:
        # Fetch starting address
        if project == LOADER:
            STARTING_ADDRESS = LOADER_APP_START_ADDRESS
        elif project == EXCAVATOR:
            STARTING_ADDRESS = EXCAVATOR_APP_START_ADDRESS
        elif project == TIPPER:
            STARTING_ADDRESS = TIPPER_APP_START_ADDRESS
        elif project == DUMPER:
            STARTING_ADDRESS = DUMPER_APP_START_ADDRESS
        elif project == GTRUCK:
            STARTING_ADDRESS = GTRUCK_APP_START_ADDRESS
        elif project == BOOTLOADER:
            STARTING_ADDRESS = BOOTLOADER_APP_START_ADDRESS
        cmd = f'{STM32PROGRAMMERCLI} {command} -w {elf_file_path} {STARTING_ADDRESS}'

    #stm32cube programmer cli interface   
    ctx.run(cmd)


def run_map(ctx, project, combine=False):
    if combine is True:
        cmd = f'python analyze_map.py --combine build/{project}/{project}.map'
    else:
        cmd = f'python analyze_map.py build/{project}/{project}.map'
    ctx.run(cmd)


def run_test(ctx, project):
    cmd = f'Pytest -v LCSAte/gpio/test_gpio.py -s'
    ctx.run(cmd)


def percentage_calculation(size=None, max_size=None):
    if size is None or max_size is None:
        raise ValueError("ValueError exception thrown")

    pct = float(( 100 ) * (size / max_size ))
    pct = "{:.2f}%".format(pct)
    return pct


def find_memory_usage(start_adddress=None, section_data=None, memor_type=None):
    count = 0
    usage = 0
    section_data_length = len(section_data)
    if memor_type == RAM:
        while (count < (section_data_length-1)):   
            if section_data[count][0:4] == start_adddress[0:4]:
                usage = usage + (int(section_data[count+3],16))
            count = count + 1
        return usage
    elif memor_type == FLASH or memor_type == QUADSPI or memor_type == SDRAM:
        while (count < (section_data_length-1)):   
            if section_data[count][0:4] == start_adddress[0:4]:
                usage = usage + (int(section_data[count+3],16))
                break
            count = count + 1
        return usage


def move_and_rename_doxygen_files(project=None, folder_name=None, file_name=None, file_format=None):
    doxyfile_path = project + "/Doxygen"
    file_path = project + "/Doxygen/" + folder_name + "/" + file_name + file_format
    shutil.move(file_path, doxyfile_path)
    
    doxyfile_path = project + "/Doxygen/" + file_name + file_format
    file_path = project + "/Doxygen/" + project + file_format
    os.remove(file_path)
    os.rename(doxyfile_path,file_path)
    
    doxyfile_path = project + "/Doxygen/" + folder_name
    os.rmdir(doxyfile_path)


@task(help={
    "project" : "The project to build (same as folder name)"
})
def build(ctx, project=None):
    """Build all/specific project"""
    check_project(project=project)
    if project.lower() == "all":
        for project in SUPPORTED_PROJECTS:
            run_make(ctx=ctx, project=project)
    else:
        run_make(ctx=ctx, project=project)


@task(help={
    "project" : "The project to clean (same as folder name)"
})
def clean(ctx, project=None):
    """Clean all/specific project"""
    check_project(project=project)
    run_clean(ctx=ctx)


@task(help={
    "project" : "The project to beautify (code formatter using astyle)",
    "check" : "If set to true (false by default), runs a dry run without modifying the files"
})
def beautify(ctx, project=None, check=False):
    """Beautifies the project mentioned. It uses astyle to perform one true brace style

    Examples:
        # Beautify the project
        $ invoke beautify --project=<project_name>
        $ invoke beautify --project=loader_prod
        $ invoke beautify -c -p all
    """
    check_project(project=project)
    if project.lower() == "all":
        for project in SUPPORTED_PROJECTS:
            run_astyle(ctx=ctx, project=project, check=check)
    else:
        run_astyle(ctx=ctx, project=project, check=check)


@task(help={
    "project" : "The project to run static analysis on (lint using cppcheck)",
})
def lint(ctx, project=None):
    """Misra C compliance check. It uses cppcheck with misra coding guidelines

    Examples:
        # Static analysis the project
        $ invoke lint --project=<project_name>
        $ invoke lint --project=loader_prod
        $ invoke lint -p all
    """
    check_project(project=project)
    if project.lower() == "all":
        for project in SUPPORTED_PROJECTS:
            run_cppcheck(ctx=ctx, project=project)
    else:
        run_cppcheck(ctx=ctx, project=project)


@task(help={
    "project" : "The project to size (same as folder name)",
})
def size(ctx, project=None):
    """To check the size of the code

    Examples:
        $ invoke size --project=<project_name>
    """
    check_project(project=project)
    if project.lower() == "all":
        for project in SUPPORTED_PROJECTS:
            run_size(ctx=ctx, project=project)
    else:
        run_size(ctx=ctx, project=project)
 
 
@task(help={
    "project" : "The project to build as html/pdf (same as folder name)",
})
def doxygen(ctx, project=None):
    """To read the source code by html view/pdf view

    Examples:
        $ invoke doxygen --project=<project_name>
    """
    check_project(project=project)
    if project.lower() == "all":
        for project in SUPPORTED_PROJECTS:
            run_doxygen(ctx=ctx, project=project)
    else:
        run_doxygen(ctx=ctx, project=project)


@task(help={
    "project" : "The project to flash in target board",
})
def flash(ctx, project=None, interface=None, config=None, exl=False):
    """To flash the bin file in target board

    Examples:
        $ invoke flash --project=<project_name> --interface=swd --config=<swd_frequency>
        $ invoke flash --project=<project_name> --interface=usb --config=<usb_port>
        $ invoke flash --project=<project name> --interface=usb --config=<swd frequency> --exl
    """
    check_project(project=project)
    if project.lower() == "all":
        for project in SUPPORTED_PROJECTS:
            run_flash(ctx=ctx, project=project, interface=interface, config=config, exl=exl)
    else:
        run_flash(ctx=ctx, project=project, interface=interface, config=config, exl=exl)


@task(help={
    "project" : "The project to map using GNU linker file (same as folder name)",
})
def map(ctx, project=None, combine=False):
    """To map the source code using GNU linker file

    Examples:
        $ invoke map --project=<project_name>
    """
    check_project(project=project)
    if project.lower() == "all":
        for project in SUPPORTED_PROJECTS:
            run_map(ctx=ctx, project=project, combine=combine)
    else:
        run_map(ctx=ctx, project=project, combine=combine)


@task(help={
    "project" : "The project peripherals add to be test",
})
def test(ctx, project=None):
    """The selected project peripherals add to be test

    Examples:
        $ invoke test --project=<project_name>
    """
    check_project(project=project)
    if project.lower() == "all":
        for project in SUPPORTED_PROJECTS:
            run_test(ctx=ctx, project=project)
    else:
        run_test(ctx=ctx, project=project)

    
# Add all tasks to the namespace
ns = Collection(build, clean, beautify, lint, size, doxygen, flash, map, test)
# Configure every task to act as a shell command
#   (will print colors, allow interactive CLI)
# Add our extra configuration file for the project
config = Config(defaults={"run": {"pty": False}})
ns.configure(config)