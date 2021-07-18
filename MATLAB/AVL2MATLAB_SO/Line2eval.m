function Out = Line2eval(Lines)
NOofEqual = 0;
for i = 1 : length(Lines)
    if Lines(i) == '='
        NOofEqual = NOofEqual + 1;
    end
end
evalstr = ' %s %s %s | ';
for i = 1 : NOofEqual
    evalstr = [evalstr '%s = %f '];
end
raw = textscan(Lines(:),evalstr);
evalstr = '';
for i = 1 : NOofEqual
    evalstr = [evalstr 'aero.%s(CaseNo) = %f; '];
end

switch NOofEqual
    case 2
        raw = textscan(Lines(:),' %s %s %s | %s = %f %s = %f ');
        Out = sprintf(evalstr,raw{4}{1},raw{5},raw{6}{1},raw{7});
    case 3
        raw = textscan(Lines(:),' %s %s %s | %s = %f %s = %f %s = %f ');
        Out = sprintf(evalstr,raw{4}{1},raw{5},raw{6}{1},raw{7},raw{8}{1},raw{9});
    case 4
        raw = textscan(Lines(:),' %s %s %s | %s = %f %s = %f %s = %f %s = %f ');
        Out = sprintf(evalstr,raw{4}{1},raw{5},raw{6}{1},raw{7},raw{8}{1},raw{9},raw{10}{1},raw{11});
end
end

