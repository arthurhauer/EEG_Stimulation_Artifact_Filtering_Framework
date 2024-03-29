function [snr,f] = snr_estimation(y,yl,Fs,windowValue)
    if nargin>3
        window=windowValue;
    else if nargin==3
        window=kaiser(256,5);
        else
            error('N�mero inv�lido de par�metros');
            return
        end
    end
    [csd,f1]=cpsd(y,yl,window,[],[],Fs);
    [psd,f2]=pwelch(y,window,[],[],Fs);
    tCsd=abs(csd);
    snr=(psd-tCsd)./tCsd;
    f=f1;
end

