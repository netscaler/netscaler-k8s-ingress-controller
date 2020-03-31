mkdir .temp
cp *.yaml .temp/
source values.sh
sed -i "s,\`CIC_IMAGE\`,$CIC_IMAGE,g" .temp/*.yaml
sed -i "s/\`VPX_IP\`/$VPX_IP/g" .temp/*.yaml
sed -i "s,\`CPX_IMAGE\`,$CPX_IMAGE,g" .temp/*.yaml
sed -i "s/\`VPX_VIP\`/$VPX_VIP/g" .temp/*.yaml
sed -i "s,\`EXPORTER\`,$EXPORTER,g" .temp/*.yaml
sed -i "s,\`VPX_PASSWORD\`,$VPX_PASSWORD,g" .temp/*.yaml
kubectl create -f .temp/monitoring.yaml
helm install prometheus-adapter/ --name cpx-prom-adapter
kubectl create -f .temp/rbac.yaml
kubectl create -f .temp/guestbook-all-in-one.yaml
kubectl create -f .temp/cic-vpx.yaml
kubectl create -f .temp/ingress_vpx.yaml
kubectl create -f .temp/ingress_cpx.yaml
kubectl create -f .temp/cpx.yaml
kubectl create -f .temp/hpa.yaml 
