resource "null_resource" "pcluster_create" {
    depends_on = [
        null_resource.upload_s3_installation
    ]
    //    triggers = {
    //        always_run = timestamp()
    //    }
    provisioner "local-exec" {
//        command = "pcluster create -c ${path.module}/config slurm-cluster"
        command = "echo 'creating the cluster'"
    }
}
