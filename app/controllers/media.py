from ferris import Controller, scaffold, route, route_with
from ferris.components.upload import Upload
from app.models.media_uploader import MediaUploader
import logging


class Media(Controller):
    class Meta:
        prefixes = ('api', 'admin')
        components = (scaffold.Scaffolding, Upload,)
        cloud_storage_bucket = "cs-intranet-storage-demo"
        Model = MediaUploader
        pagination_limit = 20

    add = scaffold.add
    edit = scaffold.edit
    list = scaffold.list
    view = scaffold.view
    delete = scaffold.delete

    @route_with('/api/media/get_upload_url')
    def upload_url(self):
        data = {
            "upload_url": self.components.upload.generate_upload_url(
            uri=self.uri('media:complete'))
        }
        return self.util.stringify_json(data)

    @route
    def complete(self):
        serving_urls = []
        uploads = self.components.upload.get_uploads()
        tags = "self.request.params['tags']"
        files = uploads.get('file')
        for blobinfo in files:
            MediaUploader.create(file=blobinfo.key(), tags=tags)
            serving_urls.append({'filename': blobinfo.filename,
                'url': "https://storage.googleapis.com/%s" % (blobinfo.cloud_storage.gs_object_name[4:]),
                'content_type': blobinfo.content_type,
                'tags': tags
                })
        self.context['serving_urls'] = serving_urls
