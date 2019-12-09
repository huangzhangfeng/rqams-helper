#define MyAppName "RQAms÷˙ ÷"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "Ricequant"
#define MyAppURL "http://www.ricequant.com/"
#define MyAppExeName "rqams-helper.exe"
#define MyAppIcon "icon.ico"

[Setup]
AppId={{A344E201-66D7-41DD-8CB6-62155FDB18FA}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
UsedUserAreasWarning=no
PrivilegesRequired=lowest
OutputBaseFilename=RQAmsHelperInstaller
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\rqams_helper\windows\resources\{#MyAppIcon}
DisableDirPage=yes

[Languages]
Name: "cn"; MessagesFile: "compiler:ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: ".\dist\rqams-helper"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ".\dist\rqams-helper\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ..\rqams_helper\windows\resources\{#MyAppIcon}; DestDir: "{app}"


[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcon}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppIcon}"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon; IconFilename: "{app}\{#MyAppIcon}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

