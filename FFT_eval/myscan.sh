PHY_NO=`iw wls35u1 info | awk '$1 == "wiphy" {print $2}'`
ATH9K_PATH=/sys/kernel/debug/ieee80211/phy$PHY_NO/ath9k_htc
SCAN_CMD="iw dev wls35u1 scan freq 2422"
ifconfig wls35u1 up
echo chanscan > $ATH9K_PATH/spectral_scan_ctl
$SCAN_CMD
cat $ATH9K_PATH/spectral_scan0 > ./output
echo disable > $ATH9K_PATH/spectral_scan_ctl
ifconfig wls35u1 down
./fft_eval_sdl ./output
