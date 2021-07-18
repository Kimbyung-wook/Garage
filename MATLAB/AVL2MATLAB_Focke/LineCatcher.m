function Out = LineCatcher(Lines)
NOofEqual = 0;
for i = 1 : length(Lines)
    if Lines(i) == '='
        NOofEqual = NOofEqual + 1;
    end
end
foreval = ' %s %s %s | ';
for i = 1 : NOofEqual
    foreval = [foreval '%s = %f '];
end

switch NOofEqual
    case 2
        Out = textscan(Lines(:),foreval);
    case 3
        Out = textscan(Lines(:),foreval);
    case 4
        Out = textscan(Lines(:),foreval);
end
end

