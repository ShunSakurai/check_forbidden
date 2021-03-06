; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Check Forbidden"
#define ProgramVersion GetFileVersion("dist\Check Forbidden.exe")

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{EF12CFBE-698F-4FAD-8C32-3ACECECBD875}}
AppName={#MyAppName}
AppVersion={#ProgramVersion}
AppVerName={#MyAppName} v.{#ProgramVersion}
AppPublisher=Shun Sakurai
AppPublisherURL=https://github.com/ShunSakurai/check_forbidden
AppSupportURL=https://github.com/ShunSakurai/check_forbidden
AppUpdatesURL=https://github.com/ShunSakurai/check_forbidden
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=check_forbidden_installer_{#ProgramVersion}
Compression=lzma
SolidCompression=yes
UsePreviousAppDir=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
Name: "{userappdata}\Check Forbidden"

[Files]
Source: "dist\{#MyAppName}.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "files\cf_template_terms.html"; DestDir: "{app}\files"; Flags: ignoreversion
Source: "files\cf_template_functions.html"; DestDir: "{app}\files"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[InstallDelete]
Type: files; Name: "{app}\cf_options.p"
Type: files; Name: "{app}\library.zip"
Type: files; Name: "{app}\python34.dll"
Type: files; Name: "{app}\tcl86t.dll"
Type: files; Name: "{app}\tk86t.dll"
Type: filesandordirs; Name: "{app}\tcl"

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppName}.exe"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
