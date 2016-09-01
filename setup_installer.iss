; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define ProgramVersion GetFileVersion("dist\Check Forbidden.exe")

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{EF12CFBE-698F-4FAD-8C32-3ACECECBD875}}
AppName=Check Forbidden
AppVersion={#ProgramVersion}
AppVerName=Check Forbidden v.{#ProgramVersion}
AppPublisher=Shun Sakurai
AppPublisherURL=https://github.com/ShunSakurai/check_forbidden
AppSupportURL=https://github.com/ShunSakurai/check_forbidden
AppUpdatesURL=https://github.com/ShunSakurai/check_forbidden
DefaultDirName={pf}\Check Forbidden
DefaultGroupName=Check Forbidden
;InfoAfterFile"Z:\Dropbox\Codes\check_forbidden\README.md
OutputBaseFilename=check_forbidden_installer_{#ProgramVersion}
Compression=lzma
SolidCompression=yes
UsePreviousAppDir=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Z:\Dropbox\Codes\check_forbidden\dist\Check Forbidden.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\Dropbox\Codes\check_forbidden\dist\library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\Dropbox\Codes\check_forbidden\dist\python34.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\Dropbox\Codes\check_forbidden\dist\tcl86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\Dropbox\Codes\check_forbidden\dist\tk86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\Dropbox\Codes\check_forbidden\dist\tcl\*"; DestDir: "{app}\tcl"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\Check Forbidden"; Filename: "{app}\Check Forbidden.exe"
Name: "{group}\{cm:UninstallProgram,Check Forbidden}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Check Forbidden"; Filename: "{app}\Check Forbidden.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Check Forbidden.exe"; Description: "{cm:LaunchProgram,Check Forbidden}"; Flags: nowait postinstall skipifsilent

