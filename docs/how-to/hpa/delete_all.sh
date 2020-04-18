kubectl delete -f .temp/monitoring.yaml
helm delete cpx-prom-adapter --purge;
kubectl delete -f .temp/rbac.yaml
kubectl delete -f .temp/guestbook-all-in-one.yaml
kubectl delete -f .temp/ingress_vpx.yaml
kubectl delete -f .temp/ingress_cpx.yaml
kubectl delete -f .temp/cpx.yaml
kubectl delete -f .temp/hpa.yaml 
kubectl delete -f .temp/cic-vpx.yaml
rm -rf .temp
