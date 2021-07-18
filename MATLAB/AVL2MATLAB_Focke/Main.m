%% Get Stab. Coeff File List
fclose all;close all; clc; clear;

Address     = 'Stab';
ModelName   = 'Focke';

DirList = dir(Address);
strs = sprintf('%s',ModelName);
strs = [strs '_V%03d.txt']
CaseNo = 1;
for i = 1:length(DirList)
% for i = 15
    raw = textscan(DirList(i).name,strs);
    if(~isempty(raw{1}))
        aero.Spd(CaseNo) = raw{1};
        CaseNo = CaseNo+1;
    end
end

for CaseNo = 1:length(aero.Spd)
    % load file
    evalstr = sprintf(strs,aero.Spd(CaseNo));
    fid = fopen([Address '\' evalstr]);
    Lines = fgetl(fid);
    LineIdx = 1; % 돌고있는 줄 수
    SecondBox = 0; % 두번째 경계선을 찾는다.
    while ischar(Lines)
%         disp(Lines);
        Lines = fgetl(fid);
        for i = 1 : length(Lines)
            if Lines(i) == ''''
                Lines(i) = ' ';
            end
        end
        Raw{LineIdx,1} = Lines;
        if (length(Lines) > 5 ) && (Lines(3) == '-')
            SecondBox = LineIdx;
        end
        LineIdx = LineIdx + 1;
    end
    fclose(fid);
    raw = textscan(Raw{SecondBox+20,1},'%s d%d'); % 조종면 찾기
    for LineIdx = 1 : length(Raw)
    % for LineIdx = 1 : 55
        if SecondBox ~= 0
            for i = 1 : length(raw{2})
                evalstr = sprintf('d%d',raw{2}(i));
                idx = strfind(Raw{LineIdx,1},evalstr);
                if ~isempty(idx)
                    Raw{LineIdx,1}(idx+1) = raw{1}{i}(1);
                end
            end
        end
    end


    % Reference
%     clc
%     CaseNo = 1;
    raw = textscan(Raw{8,1},' Sref = %f Cref = %f Bref = %f');
    ref.S       = raw{1};
    ref.C       = raw{2};
    ref.B       = raw{3};
    raw = textscan(Raw{9,1},' Xref = %f Yref = %f Zref = %f');
    ref.X       = raw{1};
    ref.Z       = raw{3};
    ref.AR      = ref.B/ref.C;
    raw = textscan(Raw{15,1},' Alpha = %f pb/2V = %f %s = %f');
    ref.Alpha0 = raw{1};
    raw = textscan(Raw{20,1},' CYtot = %f Cmtot = %f');
    aero.Cmtot(CaseNo)  = raw{2};
    raw = textscan(Raw{23,1},' CLtot = %f ');
    aero.CLtot(CaseNo)  = raw{1};
    raw = textscan(Raw{25,1},' CDvis = %f CDind = %f ');
    aero.CDo(CaseNo)    = raw{1};
    raw = textscan(Raw{27,1},' CYff = %f e = %f ');
    aero.Oswald(CaseNo) = raw{2};

    Lineidx = SecondBox + 6;
    % alpha beta
    evalstr = Line2eval(Raw{Lineidx,1}); eval(evalstr); Lineidx = Lineidx + 1;
    evalstr = Line2eval(Raw{Lineidx,1}); eval(evalstr); Lineidx = Lineidx + 1;
    evalstr = Line2eval(Raw{Lineidx,1}); eval(evalstr); Lineidx = Lineidx + 1;
    evalstr = Line2eval(Raw{Lineidx,1}); eval(evalstr); Lineidx = Lineidx + 1;
    evalstr = Line2eval(Raw{Lineidx,1}); eval(evalstr); Lineidx = Lineidx + 1;
    Lineidx = Lineidx + 3;
    % Angular Rate
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1; eval(evalstr)
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1; eval(evalstr)
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1; eval(evalstr)
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1; eval(evalstr)
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1; eval(evalstr)
    Lineidx = Lineidx + 3;
    % Control Surface
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1;eval(evalstr)
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1;eval(evalstr)
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1;eval(evalstr)
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1;eval(evalstr)
    evalstr = Line2eval(Raw{Lineidx,1}); Lineidx = Lineidx + 1;eval(evalstr)
end
%%
global Focke;
Focke.aero  = aero;
Focke.ref   = ref;
Focke.ref.da= 0.00;
Focke.ref.de= 0.00;
Focke.ref.dr= 0.00;
Focke.ref.Xcg = Focke.ref.X;
for i = 1 : length(Focke.aero)
    Focke.aero(i).CLmax = 1.58;
end