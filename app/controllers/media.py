from ferris import Controller, route, route_with
from ferris.components.upload import Upload
from app.models.certificate import Certificate
import logging


class Media(Controller):
    class Meta:
        prefixes = ('api', 'admin')
        components = (Upload,)
        Model = Certificate

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
            data = Certificate.create(file=blobinfo.key(), tags=tags)
            serving_urls.append({'filename': blobinfo.filename,
                'content_type': blobinfo.content_type,
                'tags': data.key.urlsafe()
                })
        self.context['serving_urls'] = serving_urls
