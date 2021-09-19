#pragma once
#include <windows.h>
#include <stdio.h>

#define SLOT_SERVER		("\\\\.\\mailslot\\SERVER.txt")
#define SLOT_AGENT		("\\\\.\\mailslot\\AGENT.txt")

#define SLOT_AGENT_TX		SLOT_SERVER
#define SLOT_AGENT_RX		SLOT_AGENT

#define SLOT_SERVER_TX		SLOT_AGENT
#define SLOT_SERVER_RX		SLOT_SERVER

#define IDC_OPENTX	1001
#define IDC_OPENRX	1002
#define IDC_SEND	1003
#define IDC_EDIT	1004
#define IDC_CHECK	1005
#define IDC_FUNC_SERVER	1006
#define IDC_FUNC_AGENT	1007
#define IDC_SEARCH		1008
#define RULE_SERVER		1
#define RULE_AGENT		0
#define OPEN			1
#define CLOSE			0

static HINSTANCE OPENTX_hInst;
static HINSTANCE OPENRX_hInst;
static HINSTANCE SEND_hInst;
static HINSTANCE EDIT_hInst;
static HINSTANCE CHECK_hInst;
static HINSTANCE FUNC_SERVER_hInst;
static HINSTANCE FUNC_AGENT_hInst;
static HINSTANCE SEARCH_hInst;

static HWND OPENTX_hWnd;
static HWND OPENRX_hWnd;
static HWND SEND_hWnd;
static HWND EDIT_hWnd;
static HWND CHECK_hWnd;
static HWND FUNC_SERVER_hWnd;
static HWND FUNC_AGENT_hWnd;
static HWND SEARCH_hWnd;


LRESULT CALLBACK MailSlot_WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);

class CMAIL_SLOT
{
public:
	CMAIL_SLOT();
	~CMAIL_SLOT();

public:
	bool CMAIL_SLOT::CreateCtrlWindow(char *Title, HWND Parent_hWnd);
	bool CMAIL_SLOT::OpenRX(HWND hWnd);
	bool CMAIL_SLOT::OpenTX(HWND hWnd);
	bool CMAIL_SLOT::CloseRX(HWND hWnd);
	bool CMAIL_SLOT::CloseTX(HWND hWnd);

public:
	char		info[300];
	bool		Rule = RULE_SERVER;
	bool		RX = CLOSE;
	bool		TX = CLOSE;
	char		lpszTitle[30];
	const int	X_Size = 400;
	const int   Y_Size = 200;
	const int   X_Pos = 20;
	const int   Y_Pos = 20;
	HINSTANCE	MailSlot_hInstance;
	HWND		MailSlot_hWnd;
	HANDLE hMailRX;
	HANDLE hMailTX;



};

