function [signalOut] = generate_repeatable_awgn(signalIn,snr)
S = RandStream('mt19937ar','Seed',5489);
reset(S);
signalOut = awgn(signalIn,snr,'measured',S);
reset(S);
end

