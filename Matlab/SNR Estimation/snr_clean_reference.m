function snr = snr_clean_reference( cleanReference,signal )
    snr = 10*log10(sum(cleanReference.^2)/sum((signal-cleanReference).^2));
end

