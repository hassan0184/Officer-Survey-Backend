"""Notes Related ViewSet"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.serializers import NotesSerializer
from accounts.models import Officer,Notes
from api.utils import not_found_error, sucess_response, export_notes_data_to_pdf



class NotesViewSet(APIView):
    """Notes ViewSet"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Officer Add Notes For HimSelf"""
        officer = Officer.objects.get(user=request.user)
        notes = request.data.get("notes")
        if notes is None or notes == "":
            return not_found_error("Notes Not Found")
        notes_model = Notes(notes=notes, notes_by=officer,)
        notes_model.save()
        notes = NotesSerializer(notes_model)
        return sucess_response(notes.data, 'Notes Added Successfully')

    def delete(self, request,_pk):
        """Delete Specific Note"""
        officer = Officer.objects.get(user=request.user)
        if officer is None:
            return not_found_error("Officer Not Found")
        try:
            notes_model =  Notes.objects.get(id=_pk)
            notes_model.delete()
            return sucess_response(None, 'Notes Deleted Successfully')
        except Notes.DoesNotExist:
            return not_found_error("Notes Not Found")

    def get(self, request):
        """Fetch All Notes By Officer"""
        officer = Officer.objects.get(user=request.user)
        notes = Notes.objects.filter(notes_by=officer,notes_for=None).order_by('-created_at')
        notes_serializer = NotesSerializer(notes, many=True)
        return sucess_response(notes_serializer.data, "")

    def put(self, request, _pk):
        """Update Specific Note"""
        try:
            note=Notes.objects.get(id=_pk)
            updated_notes=request.data.get("notes")
            note.notes=updated_notes
            note.save()
            notes_serializer=NotesSerializer(note, many=False)
            return sucess_response(notes_serializer.data, 'Notes have been added sucessfully')
        except Notes.DoesNotExist:
            return not_found_error("Notes not found")


class NotesForSupervisorViewSet(APIView):
    """Notes For Supervisor ViewSet"""
    permission_classes = [IsAuthenticated]

    def post(self, request, _pk):
        """Officer Add Notes For Another Officer"""
        officer= Officer.objects.get(user=request.user)
        notes= request.data.get("notes")
        if notes is None or notes == "":
            return not_found_error("Notes Not Found")
        try:
            notes_for_officer = Officer.objects.get(id=_pk)
            notes_model =Notes(notes=notes, notes_by=officer, notes_for=notes_for_officer)
            notes_model.save()
            notes =NotesSerializer(notes_model)
            return sucess_response(notes.data, 'Notes Added Successfully')
        except Officer.DoesNotExist:
            return not_found_error("Officer not found")

    def get(self,request, _pk):
        """Fetch Notes For Officer"""
        officer= Officer.objects.get(user=request.user)
        if officer:
            try:
                notes_for_officer = Officer.objects.get(id=_pk)
                notes = Notes.objects.filter(notes_for=notes_for_officer).order_by('-created_at')
                notes_serializer = NotesSerializer(notes, many=True)
                return sucess_response(notes_serializer.data, "")
            except Officer.DoesNotExist:
                return not_found_error("Officer not found")
        return not_found_error("You are not allowed to perform this action")

class ExportPdfNotesViewSet(APIView):
    """Export Pdf Notes ViewSet"""
    def get(self, request, _pk):
        """Fetch Notes In PDF"""
        hours = request.query_params.get("hours", None)
        notes_for_officer = Officer.objects.get(id=_pk)
        notes = Notes.objects.filter(notes_for=notes_for_officer).order_by('-created_at')
        return export_notes_data_to_pdf(notes, notes_for_officer, hours)
