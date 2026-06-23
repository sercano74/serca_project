import cloudinary
import cloudinary.uploader
import cloudinary.utils
from django.core.management.base import BaseCommand
from projects.models import Project
from cloudinary.models import CloudinaryField
from django.conf import settings


class Command(BaseCommand):
    help = "Asigna una imagen de Cloudinary a una obra usando su public_id"

    def add_arguments(self, parser):
        parser.add_argument("project_title", nargs="?", type=str, help="Título exacto de la obra")
        parser.add_argument("--public-id", type=str, help="Public ID de la imagen en Cloudinary (ej: SERCA/carwash1_zgddx3)")
        parser.add_argument("--image-url", type=str, help="URL completa de Cloudinary para extraer el public_id")
        parser.add_argument("--list-projects", action="store_true", help="Listar todas las obras y su estado de imagen")
        parser.add_argument("--list-cloudinary", action="store_true", help="Listar imágenes disponibles en Cloudinary")

    def handle(self, *args, **options):
        if options["list_projects"]:
            self._list_projects()
            return

        if options["list_cloudinary"]:
            self._list_cloudinary_images()
            return

        if options["image_url"]:
            public_id = self._extract_public_id_from_url(options["image_url"])
            if not public_id:
                self.stderr.write(self.style.ERROR("No se pudo extraer public_id de la URL"))
                return
            options["public_id"] = public_id

        if not options["project_title"]:
            self.stderr.write(self.style.ERROR("Debes especificar el título de la obra o usar --list-projects"))
            return

        if not options["public_id"]:
            self.stderr.write(self.style.ERROR("Debes especificar --public-id o --image-url"))
            return

        self._assign_image(options["project_title"], options["public_id"])

    def _extract_public_id_from_url(self, url: str) -> str | None:
        """
        De una URL como:
        https://res.cloudinary.com/dtcskupwr/image/upload/v1782248978/SERCA/carwash1_zgddx3.png
        extrae: SERCA/carwash1_zgddx3
        """
        try:
            # Buscar /upload/v<version>/ y tomar lo que sigue
            import re
            match = re.search(r"/upload/(?:v\d+/)?(.+?)(?:\.\w+)?$", url)
            if match:
                # Quitar extensión .png, .jpg, etc
                public_id = match.group(1)
                # Remover extensión si existe
                public_id = re.sub(r"\.\w+$", "", public_id)
                return public_id
        except Exception:
            pass
        return None

    def _list_projects(self):
        projects = Project.objects.all()
        if not projects:
            self.stdout.write(self.style.WARNING("No hay obras registradas"))
            return

        self.stdout.write(self.style.SUCCESS(f"Obras ({projects.count()}):"))
        for p in projects:
            status = f"image.url={p.image.url}" if p.image else "SIN IMAGEN"
            self.stdout.write(f"  ID={p.pk} | '{p.title}' | {status}")

    def _list_cloudinary_images(self):
        try:
            result = cloudinary.api.resources(type="upload", prefix="SERCA/", max_results=100)
            resources = result.get("resources", [])
            if not resources:
                self.stdout.write(self.style.WARNING("No se encontraron imágenes en la carpeta SERCA/"))
                return

            self.stdout.write(self.style.SUCCESS(f"Imágenes en Cloudinary (carpeta SERCA/):"))
            for r in resources:
                self.stdout.write(f"  {r['public_id']:50s}  {r['url']}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error consultando Cloudinary: {e}"))

    def _assign_image(self, project_title: str, public_id: str):
        try:
            project = Project.objects.get(title=project_title)
        except Project.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"No se encontró la obra '{project_title}'"))
            self._list_projects()
            return

        # Asignar el public_id al campo image
        project.image = public_id
        project.save(update_fields=["image"])

        # Refrescar el objeto desde BD para que CloudinaryField lo convierta a CloudinaryResource
        project.refresh_from_db()

        url = project.image.url if project.image else "⚠️ Sin URL (imagen None)"
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Imagen asignada correctamente a '{project.title}'\n"
                f"  public_id: {public_id}\n"
                f"  URL: {url}"
            )
        )
