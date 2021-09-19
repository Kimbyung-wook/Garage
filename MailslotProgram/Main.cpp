#include <windows.h>
#include <iostream>
#include <fstream>
#include <conio.h>
#include <stdio.h>

#ifndef _USE_OLD_OSTREAMS
	using namespace std;
#endif

#include "resource.h"
#include "Main.h"
#include "MailSlot.h"
#include "guicon.h"
#include <crtdbg.h>
ATOM			 MyRegisterClass(HINSTANCE hInstance);
BOOL			 InitInstance(HINSTANCE hInstance, int nCmdShow);
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
HINSTANCE		 g_hInst;
HINSTANCE		 hInst;
LPCSTR			 lpszClass = "MailSlot Program";
HWND			 hWnd;
HWND			 CONSOLE_hWnd;
HANDLE			 hConsole;

CMAIL_SLOT CMail_Slot;


int APIENTRY WinMain(HINSTANCE hInstance,HINSTANCE hPrevInstance,LPTSTR lpCmdLine,int nCmdShow)
{
	MSG Message;

	MyRegisterClass(hInstance);					//Set window property
	if (!InitInstance(hInstance, nCmdShow))		//Set window
		return FALSE;

	CMail_Slot.CreateCtrlWindow("MailSlot_Ctrl", hWnd);

	// Create Window object


	// Get Message from other devices
	while (GetMessage(&Message, 0, 0, 0)){
		TranslateMessage(&Message);
		DispatchMessage(&Message);
	}
	return Message.wParam;
}
ATOM MyRegisterClass(HINSTANCE hInstance)
{
	WNDCLASS WndClass;

	WndClass.cbClsExtra		= 0;
	WndClass.cbWndExtra		= 0;
	WndClass.hbrBackground	= (HBRUSH)GetStockObject(WHITE_BRUSH);
	WndClass.hCursor		= LoadCursor(NULL, IDC_ARROW);
	//WndClass.hIcon			= LoadIcon(NULL, IDI_APPLICATION);
	WndClass.hIcon			= LoadIcon(NULL, IDI_APPLICATION);
	WndClass.hInstance = hInstance;
	WndClass.lpfnWndProc	= (WNDPROC)WndProc;
	WndClass.lpszClassName	= lpszClass;
	WndClass.lpszMenuName	= NULL;
	WndClass.style			= CS_HREDRAW | CS_VREDRAW;

	// Declare Window Class
	return RegisterClass(&WndClass);
}
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
	int X_Size = Cx;
	int Y_Size = Cy;
	hInst = hInstance; // 인스턴스 핸들을 전역 변수에 저장합니다.

	hWnd = CreateWindow(lpszClass, lpszClass, WS_OVERLAPPEDWINDOW,
		CW_USEDEFAULT, 0, X_Size, Y_Size, NULL, NULL, hInstance, NULL);

	if (!hWnd)
		return FALSE;

	ShowWindow(hWnd, nCmdShow);
	SetWindowPos(hWnd, HWND_TOP, 0, 0, X_Size, Y_Size, SWP_FRAMECHANGED);
	UpdateWindow(hWnd);

	return TRUE;
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT iMessage, WPARAM wParam, LPARAM lParam)
{
	HDC hdc;
	PAINTSTRUCT ps;
	LONG lStyle;
	COORD Console_COORD;
	SMALL_RECT Console_rc;
	switch (iMessage)
	{
	case WM_CREATE:
		#ifdef _DEBUG
			RedirectIOToConsole();
			CONSOLE_hWnd = GetConsoleHwnd();
			SetParent((HWND)CONSOLE_hWnd, hWnd);
			SetWindowPos((HWND)CONSOLE_hWnd, HWND_TOP, 5, 90, Cx-25, 500, SWP_FRAMECHANGED);//Console Window size
			lStyle = GetWindowLong(CONSOLE_hWnd, GWL_STYLE);
			lStyle &= ~(WS_CAPTION | WS_EX_APPWINDOW | WS_EX_WINDOWEDGE | WS_EX_DLGMODALFRAME);
			SetWindowLong(CONSOLE_hWnd, GWL_STYLE, lStyle);
			//system("MODE CON COLS=49 LINES=20");
			/*hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
			Console_rc.Top = 0;
			Console_rc.Left = 0;
			Console_rc.Bottom = 20;
			Console_rc.Right = 40;
			SetConsoleWindowInfo(hConsole, TRUE, &Console_rc);
			Console_COORD.X = 10;
			Console_COORD.Y = 10;
			SetConsoleScreenBufferSize(hConsole, Console_COORD);*/
		#endif
		break;
	case WM_DESTROY:
		PostQuitMessage(0);
		return 0;
	}
	return(DefWindowProc(hWnd, iMessage, wParam, lParam));
}