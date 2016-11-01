def get_permission_codename(model, perm):
    return "%s.%s_%s" % (model._meta.app_label, perm, model._meta.model_name)
