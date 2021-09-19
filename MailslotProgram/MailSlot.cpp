#include "MailSlot.h"


CMAIL_SLOT::CMAIL_SLOT()
{
}


CMAIL_SLOT::~CMAIL_SLOT()
{
}

extern CMAIL_SLOT CMail_Slot;
void FileList(char *Path)
{
	HANDLE hSearch;
	WIN32_FIND_DATA wfd;
	BOOL bResult = TRUE;
	char szDrive[_MAX_DRIVE];
	char szDir[MAX_PATH];
	char szNewpath[MAX_PATH];
	char szFilename[_MAX_FNAME];
	char szExt[_MAX_EXT];

	printf("Current Dir : %s\n", Path);
	hSearch = FindFirstFile(Path, &wfd);
	if (hSearch == INVALID_HANDLE_VALUE)
		return;
	_splitpath_s(Path, szDrive, _MAX_DRIVE,szDir,_MAX_DIR,szFilename,_MAX_FNAME,szExt,_MAX_EXT);
	while (bResult){
		if (wfd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY){
			if (strcmp(wfd.cFileName, ".") && strcmp(wfd.cFileName, "..")){
				sprintf_s(szNewpath, "%s%s%s\\*.*", szDrive, szDir, wfd.cFileName);
				FileList(szNewpath);
			}
		}
		else
			printf("\t%s\n",wfd.cFileName);
		bResult = FindNextFile(hSearch, &wfd);
	}
	FindClose(hSearch);
}
bool CMAIL_SLOT::OpenRX(HWND hWnd)
{
	if (CMail_Slot.Rule == RULE_SERVER){
		CMail_Slot.hMailRX = CreateMailslot(SLOT_SERVER, 0, 0, NULL);
		if (CMail_Slot.hMailRX == INVALID_HANDLE_VALUE){
			MessageBox(hWnd, "Failed to open Server RX", "Error", MB_OK);
			return 0;
		}
		else{
			CMail_Slot.RX = OPEN;
			SetWindowText(OPENRX_hWnd, "CloseRx");
			printf("Server RX open : %s\n",SLOT_SERVER);
		}
		return 1;
	}
	else{
		CMail_Slot.hMailRX = CreateMailslot(SLOT_AGENT, 0, 0, NULL);
		if (CMail_Slot.hMailRX == INVALID_HANDLE_VALUE){
			MessageBox(hWnd, "Failed to open Agent RX", "Error", MB_OK);
			return 0;
		}
		else{
			CMail_Slot.RX = OPEN;
			SetWindowText(OPENRX_hWnd, "CloseRx");
			printf("Agent RX open : %s\n", SLOT_AGENT);
		}
		return 1;
	}
}
bool CMAIL_SLOT::OpenTX(HWND hWnd)
{
	if (CMail_Slot.Rule == RULE_SERVER){
		CMail_Slot.hMailTX = CreateFile(SLOT_AGENT, GENERIC_WRITE, FILE_SHARE_READ, NULL,
			OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
		if (CMail_Slot.hMailTX == INVALID_HANDLE_VALUE){
			MessageBox(hWnd, "Failed to open Server TX", "Error", MB_OK);
			return 0;
		}
		else{
			CMail_Slot.TX = OPEN;
			SetWindowText(OPENTX_hWnd, "CloseTx");
			printf("Server TX open : %s\n", SLOT_AGENT);
		}
		return 1;
	}
	else{
		CMail_Slot.hMailTX = CreateFile(SLOT_SERVER, GENERIC_WRITE, FILE_SHARE_READ, NULL,
			OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
		if (CMail_Slot.hMailTX == INVALID_HANDLE_VALUE){
			MessageBox(hWnd, "Failed to open Agent TX", "Error", MB_OK);
			return 0;
		}
		else{
			CMail_Slot.TX = OPEN;
			SetWindowText(OPENTX_hWnd, "CloseRx");
			printf("Agent TX open : %s\n", SLOT_SERVER);
		}
		return 1;
	}
}
bool CMAIL_SLOT::CloseRX(HWND hWnd)
{
	if (CMail_Slot.RX == CLOSE)
		return 0;
	if (CloseHandle(hMailRX)){
		SetWindowText(OPENRX_hWnd, "OpenRx");
		CMail_Slot.RX = CLOSE;
		printf("Close RX\n");
		return 1;
	}
	else{
		MessageBox(hWnd, "Failed to close RX", "Error", MB_OK);
		return 0;
	}
}
bool CMAIL_SLOT::CloseTX(HWND hWnd)
{
	//is it open? and can close handle?
	if (CMail_Slot.TX == CLOSE)
		return 0;
	if (CloseHandle(hMailTX)){
		SetWindowText(OPENTX_hWnd, "OpenTx");
		CMail_Slot.TX = CLOSE;
		printf("Close TX\n");
		return 1;
	}
	else{
		MessageBox(hWnd, "Failed to close TX", "Error", MB_OK);
		return 0;
	}
}
LRESULT CALLBACK MailSlot_WndProc(HWND hWnd, UINT iMessage, WPARAM wParam, LPARAM lParam)
{
	HDC hdc;
	PAINTSTRUCT ps;
	DWORD lBytesWritten = 0;
	DWORD lBytesRed = 0;
	char cGetString[200] = "";
	char cSendString[200] = "";

	switch (iMessage)
	{
	case WM_CREATE:
		OPENTX_hWnd = CreateWindow("button", "OpenTx", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
			0, 25, 60, 25, hWnd, (HMENU)IDC_OPENTX, OPENTX_hInst, NULL);
		OPENRX_hWnd = CreateWindow("button", "OpenRx", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
			60, 25, 60, 25, hWnd, (HMENU)IDC_OPENRX, OPENRX_hInst, NULL);
		CHECK_hWnd = CreateWindow("button", "Check", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
			120, 25, 60, 25, hWnd, (HMENU)IDC_CHECK, CHECK_hInst, NULL);
		SEARCH_hWnd = CreateWindow("button", "Search", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
			180, 25, 60, 25, hWnd, (HMENU)IDC_SEARCH, SEARCH_hInst, NULL);
		SEND_hWnd = CreateWindow("button", "Send", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
			0, 50, 60, 25, hWnd, (HMENU)IDC_SEND, SEND_hInst, NULL);
		EDIT_hWnd = CreateWindow("edit", "", WS_CHILD | WS_VISIBLE | WS_BORDER,
			60, 50, 340, 25, hWnd, (HMENU)IDC_EDIT, EDIT_hInst, NULL);

		FUNC_SERVER_hWnd = CreateWindow("button", "Server", WS_CHILD | WS_VISIBLE | BS_AUTORADIOBUTTON,
			330, 0, 70, 25, hWnd, (HMENU)IDC_FUNC_SERVER, FUNC_SERVER_hInst, NULL);
		FUNC_AGENT_hWnd = CreateWindow("button", "Agent", WS_CHILD | WS_VISIBLE | BS_AUTORADIOBUTTON,
			330, 25, 70, 25, hWnd, (HMENU)IDC_FUNC_AGENT, FUNC_AGENT_hInst, NULL);
		CheckRadioButton(hWnd, IDC_FUNC_SERVER, IDC_FUNC_AGENT, IDC_FUNC_SERVER);
		return 0;
	case WM_COMMAND:
		switch (LOWORD(wParam))
		{
		case IDC_OPENTX:
			if (!CMail_Slot.TX)
				CMail_Slot.OpenTX(hWnd);
			else
				CMail_Slot.CloseTX(hWnd);
			break;
		case IDC_OPENRX:
			if (!CMail_Slot.RX)
				CMail_Slot.OpenRX(hWnd);
			else
				CMail_Slot.CloseRX(hWnd);
			break;
		case IDC_CHECK:
			if (!CMail_Slot.RX){
				MessageBox(hWnd, "Please open RX", "ERROR", MB_OK);
				break;
			}
			if (!ReadFile(CMail_Slot.hMailRX, cGetString, sizeof(cGetString), &lBytesRed, NULL))
			{
				printf("Read %2d : %s\n", lBytesRed, cGetString);
				MessageBox(hWnd, "No Message", "ERROR", MB_OK);
				break;
			}
			printf("Read %2d : %s\n", lBytesRed, cGetString);
			break;
		case IDC_SEARCH:
			char Path[MAX_PATH];
			GetCurrentDirectory(MAX_PATH, Path);
			strcat_s(Path, "\\*.*");
			FileList(Path);
			break;
		case IDC_SEND:
			if (GetDlgItemText(hWnd, IDC_EDIT, cSendString, sizeof(cSendString)) == -1)
			{
				printf("Send  0 : ERROR\n");
				break;
			}
			if (!WriteFile(CMail_Slot.hMailTX, cSendString, strlen(cSendString), &lBytesWritten, NULL))
			{
				MessageBox(hWnd, "Failed to send", "ERROR", MB_OK);
				break;
			}
			printf("Send %2d : %s\n", lBytesWritten, cSendString);
			break;
		case IDC_FUNC_SERVER:
			if (CMail_Slot.Rule == RULE_AGENT){
				CMail_Slot.CloseTX(hWnd);
				CMail_Slot.CloseRX(hWnd);
				CMail_Slot.Rule = RULE_SERVER;
				printf("RULE : SERVER\n");
			}
			break;
		case IDC_FUNC_AGENT:
			if (CMail_Slot.Rule == RULE_SERVER){
				CMail_Slot.CloseTX(hWnd);
				CMail_Slot.CloseRX(hWnd);
				CMail_Slot.Rule = RULE_AGENT;
				printf("RULE : AGENT\n");
			}
			break;
		}

		return 0;
	case WM_PAINT:
		hdc = BeginPaint(hWnd, &ps);
		EndPaint(hWnd, &ps);
		return 0;
	case WM_DESTROY:
		PostQuitMessage(0);
		return 0;
	}
	return(DefWindowProc(hWnd, iMessage, wParam, lParam));
}
bool CMAIL_SLOT::CreateCtrlWindow(char *Title, HWND Parent_hWnd)
{
	WNDCLASS	WndClass;
	DWORD		dwStyle;
	DWORD		dwExStyle;

	sprintf_s(CMAIL_SLOT::lpszTitle, "MailSlot_Ctrl");
	WndClass.style			= CS_HREDRAW | CS_VREDRAW | CS_OWNDC;
	WndClass.lpfnWndProc	= (WNDPROC)(MailSlot_WndProc);
	WndClass.cbClsExtra		= 0;
	WndClass.cbWndExtra		= 0;
	WndClass.hInstance		= CMAIL_SLOT::MailSlot_hInstance;
	WndClass.hCursor		= LoadCursor(NULL, IDC_ARROW);
	WndClass.hIcon			= LoadIcon(NULL, IDI_APPLICATION);
	WndClass.hbrBackground	= (HBRUSH)(COLOR_WINDOW + 1);
	WndClass.lpszMenuName	= NULL;
	WndClass.lpszClassName	= CMAIL_SLOT::lpszTitle;
	if (!RegisterClass(&WndClass))
	{
		MessageBox(NULL, "Failed to register the window class", "ERROR", MB_OK | MB_ICONEXCLAMATION);
		return FALSE;
	}

	dwExStyle	= WS_EX_APPWINDOW | WS_EX_WINDOWEDGE | WS_EX_DLGMODALFRAME | WS_EX_TRANSPARENT;
	dwStyle		= WS_CHILDWINDOW;

	RECT		WndRect;
	WndRect.top	= (long)0;
	WndRect.bottom = (long)200;
	WndRect.left = (long)0;
	WndRect.right = (long)410;
	AdjustWindowRectEx(&WndRect, dwStyle, FALSE, dwExStyle);
	if (!(CMAIL_SLOT::MailSlot_hWnd = CreateWindowEx(dwExStyle, CMAIL_SLOT::lpszTitle,
		Title,
		dwStyle | WS_CLIPSIBLINGS | WS_CLIPCHILDREN,
		5, 5,  // x,y
		410, 85,// cx,cy
		Parent_hWnd,//No Parent Window
		NULL, // No Menu
		CMAIL_SLOT::MailSlot_hInstance,
		NULL)))
	{
		MessageBox(NULL, "Failed to create window", "ERROR", MB_OK | MB_ICONEXCLAMATION);
		return FALSE;
	}
	ShowWindow(CMAIL_SLOT::MailSlot_hWnd, SW_SHOW);
	UpdateWindow(CMAIL_SLOT::MailSlot_hWnd);
	SetForegroundWindow(CMAIL_SLOT::MailSlot_hWnd);
	SetFocus(CMAIL_SLOT::MailSlot_hWnd);
	return TRUE;
}