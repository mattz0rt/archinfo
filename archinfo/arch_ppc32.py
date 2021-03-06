try:
    import capstone as _capstone
except ImportError:
    _capstone = None

#try:
#   import unicorn as _unicorn
#except ImportError:
#   _unicorn = None

from .arch import Arch, register_arch
from .tls import TLSArchInfo

# Note: PowerPC doesn't have pc, so guest_CIA is commented as IP (no arch visible register)
# PowerPC doesn't have stack base pointer, so bp_offset is set to -1 below
# Normally r1 is used as stack pointer

class ArchPPC32(Arch):
    def __init__(self, endness="Iend_LE"):
        super(ArchPPC32, self).__init__(endness)
        if endness == 'Iend_BE':
            self.function_prologs = {
                # stwu r1, -off(r1); mflr r0
                r"\x94\x21[\x00-\xff]{2}\x7c\x08\x02\xa6"
            }
            self.function_epilogs = {
                # mtlr reg; ... ; blr
                r"[\x00-\xff]{2}\x03\xa6([\x00-\xff]{4}){0,6}\x4e\x80\x00\x20"
            }

    bits = 32
    vex_arch = "VexArchPPC32"
    name = "PPC32"
    qemu_name = 'ppc'
    ida_processor = 'ppc'
    linux_name = 'ppc750'   # ?
    triplet = 'powerpc-linux-gnu'
    max_inst_bytes = 4
    ip_offset = 1160
    sp_offset = 20
    bp_offset = 140
    # https://www.ibm.com/developerworks/community/forums/html/topic?id=77777777-0000-0000-0000-000013836863
    # claims that r15 is the base pointer but that is NOT what I see in practice
    ret_offset = 28
    lr_offset = 1172
    syscall_num_offset = 16
    call_pushes_ret = False
    stack_change = -4
    sizeof = {'short': 16, 'int': 32, 'long': 32, 'long long': 64}
    if _capstone:
        cs_arch = _capstone.CS_ARCH_PPC
        cs_mode = _capstone.CS_MODE_32 + _capstone.CS_MODE_LITTLE_ENDIAN
    # unicorn not supported
    #uc_arch = _unicorn.UC_ARCH_PPC if _unicorn else None
    #uc_mode = (_unicorn.UC_MODE_32 + _unicorn.UC_MODE_LITTLE_ENDIAN) if _unicorn else None
    ret_instruction = "\x20\x00\x80\x4e"
    nop_instruction = "\x00\x00\x00\x60"
    instruction_alignment = 4

    function_prologs = {
        r"[\x00-\xff]{2}\x21\x94\xa6\x02\x08\x7c",     # stwu r1, -off(r1); mflr r0
    }
    function_epilogs = {
        r"\xa6\x03[\x00-\xff]{2}([\x00-\xff]{4}){0,6}\x20\x00\x80\x4e"    # mtlr reg; ... ; blr
    }

    default_register_values = [
        ( 'sp', Arch.initial_sp, True, 'global' ) # the stack
    ]
    entry_register_values = {
        'r3': 'argc',
        'r4': 'argv',
        'r5': 'envp',
        'r6': 'auxv',
        'r7': 'ld_destructor'
    }

    default_symbolic_registers = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12',
                                   'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'r22', 'r23', 'r24',
                                   'r25', 'r26', 'r27', 'r28', 'r29', 'r30', 'r31', 'sp', 'pc'] + ['f%d' % i for i in range(0, 32)]

    register_names = {
        0: 'host_evc_failaddr',
        4: 'host_evc_counter',
        8: 'pad3',
        12: 'pad4',
        16: 'r0',
        20: 'r1',
        24: 'r2',
        28: 'r3',
        32: 'r4',
        36: 'r5',
        40: 'r6',
        44: 'r7',
        48: 'r8',
        52: 'r9',
        56: 'r10',
        60: 'r11',
        64: 'r12',
        68: 'r13',
        72: 'r14',
        76: 'r15',
        80: 'r16',
        84: 'r17',
        88: 'r18',
        92: 'r19',
        96: 'r20',
        100: 'r21',
        104: 'r22',
        108: 'r23',
        112: 'r24',
        116: 'r25',
        120: 'r26',
        124: 'r27',
        128: 'r28',
        132: 'r29',
        136: 'r30',
        140: 'r31',
        144: 'v0',
        160: 'v1',
        176: 'v2',
        192: 'v3',
        208: 'v4',
        224: 'v5',
        240: 'v6',
        256: 'v7',
        272: 'v8',
        288: 'v9',
        304: 'v10',
        320: 'v11',
        336: 'v12',
        352: 'v13',
        368: 'v14',
        384: 'v15',
        400: 'v16',
        416: 'v17',
        432: 'v18',
        448: 'v19',
        464: 'v20',
        480: 'v21',
        496: 'v22',
        512: 'v23',
        528: 'v24',
        544: 'v25',
        560: 'v26',
        576: 'v27',
        592: 'v28',
        608: 'v29',
        624: 'v30',
        640: 'v31',
        656: 'v32',
        672: 'v33',
        688: 'v34',
        704: 'v35',
        720: 'v36',
        736: 'v37',
        752: 'v38',
        768: 'v39',
        784: 'v40',
        800: 'v41',
        816: 'v42',
        832: 'v43',
        848: 'v44',
        864: 'v45',
        880: 'v46',
        896: 'v47',
        912: 'v48',
        928: 'v49',
        944: 'v50',
        960: 'v51',
        976: 'v52',
        992: 'v53',
        1008: 'v54',
        1024: 'v55',
        1040: 'v56',
        1056: 'v57',
        1072: 'v58',
        1088: 'v59',
        1104: 'v60',
        1120: 'v61',
        1136: 'v62',
        1152: 'v63',
        1168: 'pc',
        1172: 'lr',
        1176: 'ctr',
        1180: 'xer_so',
        1181: 'xer_ov',
        1182: 'xer_ca',
        1183: 'xer_bc',
        1184: 'cr0_321',
        1185: 'cr0_0',
        1186: 'cr1_321',
        1187: 'cr1_0',
        1188: 'cr2_321',
        1189: 'cr2_0',
        1190: 'cr3_321',
        1191: 'cr3_0',
        1192: 'cr4_321',
        1193: 'cr4_0',
        1194: 'cr5_321',
        1195: 'cr5_0',
        1196: 'cr6_321',
        1197: 'cr6_0',
        1198: 'cr7_321',
        1199: 'cr7_0',
        1200: 'fpround',
        1201: 'dfpround',
        1202: 'pad1',
        1203: 'pad2',
        1204: 'vrsave',
        1208: 'vscr',
        1212: 'emnote',
        1216: 'cmstart',
        1220: 'cmlen',
        1224: 'nraddr',
        1228: 'nraddr_gpr2',
        1232: 'redir_sp',
        1236: 'redir_stack',
        1364: 'ip_at_syscall',
        1368: 'sprg3_ro',
        1372: 'padding1',
        1376: 'tfhar',
        1384: 'texasr',
        1392: 'tfiar',
        1400: 'texasru',
        1404: 'padding2',
    }

    registers = {
        'host_evc_failaddr': (0, 4),
        'host_evc_counter': (4, 4),
        'pad3': (8, 4),
        'pad4': (12, 4),
        'r0': (16, 4),
        'r1': (20, 4), 'sp': (20, 4),
        'r2': (24, 4),
        'r3': (28, 4),
        'r4': (32, 4),
        'r5': (36, 4),
        'r6': (40, 4),
        'r7': (44, 4),
        'r8': (48, 4),
        'r9': (52, 4),
        'r10': (56, 4),
        'r11': (60, 4),
        'r12': (64, 4),
        'r13': (68, 4),
        'r14': (72, 4),
        'r15': (76, 4), 'bp': (76, 4),
        'r16': (80, 4),
        'r17': (84, 4),
        'r18': (88, 4),
        'r19': (92, 4),
        'r20': (96, 4),
        'r21': (100, 4),
        'r22': (104, 4),
        'r23': (108, 4),
        'r24': (112, 4),
        'r25': (116, 4),
        'r26': (120, 4),
        'r27': (124, 4),
        'r28': (128, 4),
        'r29': (132, 4),
        'r30': (136, 4),
        'r31': (140, 4),
        'v0': (144, 16),
        'v1': (160, 16),
        'v2': (176, 16),
        'v3': (192, 16),
        'v4': (208, 16),
        'v5': (224, 16),
        'v6': (240, 16),
        'v7': (256, 16),
        'v8': (272, 16),
        'v9': (288, 16),
        'v10': (304, 16),
        'v11': (320, 16),
        'v12': (336, 16),
        'v13': (352, 16),
        'v14': (368, 16),
        'v15': (384, 16),
        'v16': (400, 16),
        'v17': (416, 16),
        'v18': (432, 16),
        'v19': (448, 16),
        'v20': (464, 16),
        'v21': (480, 16),
        'v22': (496, 16),
        'v23': (512, 16),
        'v24': (528, 16),
        'v25': (544, 16),
        'v26': (560, 16),
        'v27': (576, 16),
        'v28': (592, 16),
        'v29': (608, 16),
        'v30': (624, 16),
        'v31': (640, 16),
        # There's an overlap of registers for floating point, so will point to same offset
        'f0': (144, 8),
        'f1': (160, 8),
        'f2': (176, 8),
        'f3': (192, 8),
        'f4': (208, 8),
        'f5': (224, 8),
        'f6': (240, 8),
        'f7': (256, 8),
        'f8': (272, 8),
        'f9': (288, 8),
        'f10': (304, 8),
        'f11': (320, 8),
        'f12': (336, 8),
        'f13': (352, 8),
        'f14': (368, 8),
        'f15': (384, 8),
        'f16': (400, 8),
        'f17': (416, 8),
        'f18': (432, 8),
        'f19': (448, 8),
        'f20': (464, 8),
        'f21': (480, 8),
        'f22': (496, 8),
        'f23': (512, 8),
        'f24': (528, 8),
        'f25': (544, 8),
        'f26': (560, 8),
        'f27': (576, 8),
        'f28': (592, 8),
        'f29': (608, 8),
        'f30': (624, 8),
        'f31': (640, 8),
        # Resume vector registers
        'v32': (656, 16),
        'v33': (672, 16),
        'v34': (688, 16),
        'v35': (704, 16),
        'v36': (720, 16),
        'v37': (736, 16),
        'v38': (752, 16),
        'v39': (768, 16),
        'v40': (784, 16),
        'v41': (800, 16),
        'v42': (816, 16),
        'v43': (832, 16),
        'v44': (848, 16),
        'v45': (864, 16),
        'v46': (880, 16),
        'v47': (896, 16),
        'v48': (912, 16),
        'v49': (928, 16),
        'v50': (944, 16),
        'v51': (960, 16),
        'v52': (976, 16),
        'v53': (992, 16),
        'v54': (1008, 16),
        'v55': (1024, 16),
        'v56': (1040, 16),
        'v57': (1056, 16),
        'v58': (1072, 16),
        'v59': (1088, 16),
        'v60': (1104, 16),
        'v61': (1120, 16),
        'v62': (1136, 16),
        'v63': (1152, 16),
        'cia': (1168, 4), 'ip': (1168, 4), 'pc': (1168, 4),
        'lr': (1172, 4),
        'ctr': (1176, 4),
        'xer_so': (1180, 1),
        'xer_ov': (1181, 1),
        'xer_ca': (1182, 1),
        'xer_bc': (1183, 1),
        'cr0_321': (1184, 1),
        'cr0_0': (1185, 1), 'cr0': (1185, 1),
        'cr1_321': (1186, 1),
        'cr1_0': (1187, 1), 'cr1': (1187, 1),
        'cr2_321': (1188, 1),
        'cr2_0': (1189, 1), 'cr2': (1189, 1),
        'cr3_321': (1190, 1),
        'cr3_0': (1191, 1), 'cr3': (1191, 1),
        'cr4_321': (1192, 1),
        'cr4_0': (1193, 1), 'cr4': (1193, 1),
        'cr5_321': (1194, 1),
        'cr5_0': (1195, 1), 'cr5': (1195, 1),
        'cr6_321': (1196, 1),
        'cr6_0': (1197, 1), 'cr6': (1197, 1),
        'cr7_321': (1198, 1),
        'cr7_0': (1199, 1), 'cr7': (1199, 1),
        'fpround': (1200, 1),
        'dfpround': (1201, 1),
        'pad1': (1202, 1),
        'pad2': (1203, 1),
        'vrsave': (1204, 4),
        'vscr': (1208, 4),
        'emnote': (1212, 4),
        'cmstart': (1216, 4),
        'cmlen': (1220, 4),
        'nraddr': (1224, 4),
        'nraddr_gpr2': (1228, 4),
        'redir_sp': (1232, 4),
        'redir_stack': (1236, 128),
        'ip_at_syscall': (1364, 4),
        'sprg3_ro': (1368, 4),
        'padding1': (1372, 4),
        'tfhar': (1376, 8),
        'texasr': (1384, 8),
        'tfiar': (1392, 8),
        'texasru': (1400, 4),
        'padding2': (1404, 4),
    }

    argument_registers = {
        registers['r3'],
        registers['r4'],
        registers['r5'],
        registers['r6'],
        registers['r7'],
        registers['r8'],
        registers['r9'],
        registers['r10'],
        registers['f1'],
        registers['f2'],
        registers['f3'],
        registers['f4'],
        registers['f5'],
        registers['f6'],
        registers['f7'],
        registers['f8'],
    }

    argument_register_positions = {
        registers['r3']: 0,
        registers['r4']: 1,
        registers['r5']: 2,
        registers['r6']: 3,
        registers['r7']: 4,
        registers['r8']: 5,
        registers['r9']: 6,
        registers['r10']: 7,
        registers['f1']: 0,
        registers['f2']: 1,
        registers['f3']: 2,
        registers['f4']: 3,
        registers['f5']: 4,
        registers['f6']: 5,
        registers['f7']: 6,
        registers['f8']: 7,
    }

    got_section_name = '.plt'
    ld_linux_name = 'ld.so.1'
    elf_tls = TLSArchInfo(1, 52, [], [48], [], 0x7000, 0x8000)

register_arch([r'.*p\w*pc.*'], 32, 'any', ArchPPC32)
