function [snr,f] = snr_estimation(y,yl,Fs,windowValue)
    if nargin>3
        window=windowValue;
    else if nargin==3
        window=kaiser(256,5);
        else
            error("Número inválido de parâmetros");
            return
        end
    end
    [csd,f1]=cpsd(y,yl,window);
    [psd,f2]=pwelch(y,window);
    snr=(psd-abs(csd))/abs(csd);
    f=f1;
end

