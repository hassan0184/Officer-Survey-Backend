"""Questions Related ViewSet"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.serializers import QuestionSerializer
from accounts.models import Officer
from api.utils import not_found_error, sucess_response
from survey.models import Question, Choice


class QuestionViewSet(APIView):
    """Question ViewSet"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Add Questions In Survey"""
        officer = Officer.objects.get(user=request.user)
        question = request.data.get("question")
        question_type = request.data.get("type")
        required = request.data.get("required")
        choices = request.data.get("choices")
        count = Question.objects.filter(survey=officer.department.survey)
        if question is None or question == "":
            return not_found_error("Question Not Found")
        if question_type is None or question_type == "":
            return not_found_error("Type Not Found")
        if required is None:
            return not_found_error("Required Not Found")
        question_model = Question(question=question, type=question_type,
        survey=officer.department.survey, required=required, order=len(count)+1)
        question_model.save()
        for choice in choices:
            if choice.get('choice') is None:
                return not_found_error("Choice Not Found")
            choice_model = Choice(
                choice=choice.get('choice'),
                show_comment_box=choice.get('show_comment_box'),
                comment_box_place_holder=choice.get('comment_box_place_holder'),
                question=question_model)
            choice_model.save()
        question = QuestionSerializer(question_model)
        return sucess_response(question.data, 'Question Added Successfully')

    def put(self, request, _pk):
        """Update Questions In Survey"""
        try:
            officer = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")
        question = request.data.get("question")
        question_type = request.data.get("type")
        choices = request.data.get("choices")
        required = request.data.get("required")
        delete_choices = request.data.get("delete_choices")
        if question is None:
            return not_found_error("Question Not Found")
        if question_type is None:
            return not_found_error("Type Not Found")
        if required is None:
            return not_found_error("Required Not Found")
        try:
            question_model = Question.objects.get(id=_pk)
        except Question.DoesNotExist:
            return not_found_error("Question Not Found")
        question_model.question = question
        question_model.type = question_type
        question_model.required = required
        question_model.save()
        for choice in choices:
            if choice.get('id') is None:
                return not_found_error("Choice Not Found")
            if(choice.get('is_new') is not None and choice.get('is_new')):
                choice = Choice(
                    choice=choice.get('choice'),
                    show_comment_box=choice.get('show_comment_box'),
                    comment_box_place_holder=choice.get('comment_box_place_holder'),
                    question=question_model)
                choice.save()
                break
            try:
                choice_model = Choice.objects.get(id=choice.get('id'))
            except Choice.DoesNotExist:
                return not_found_error("Choice Not Found")
            if choice.get('choice') is None:
                return not_found_error("Choice Not Found")
            choice_model.choice=choice.get('choice')
            choice_model.show_comment_box=choice.get('show_comment_box')
            choice_model.comment_box_place_holder=choice.get('comment_box_place_holder')
            choice_model.save()
        for choice in delete_choices:
            try:
                choice_model = Choice.objects.get(id=choice)
                choice_model.delete()
            except Choice.DoesNotExist:
                pass
        question = QuestionSerializer(question_model)
        return sucess_response(question.data, 'Question Update Successfully')

    def get(self, request, _pk):
        """Fetch Specific Questions"""
        try:
            officer = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")
        try:
            question = Question.objects.get(id=_pk)
            question = QuestionSerializer(question)
            return sucess_response(question.data)
        except Question.DoesNotExist:
            return not_found_error("Question Not Found")

    def delete(self, request, _pk):
        """Delete Question"""
        try:
            officer = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")
        try:
            question_model = Question.objects.get(id=_pk)
            question_model.delete()
            return sucess_response(None, 'Question Deleted Successfully')
        except Question.DoesNotExist:
            return not_found_error("Question Not Found")

class ReorderQuestionViewSet(APIView):
    """Reorder Question ViewSet"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """Post Questions With Order Change """
        try:
            questions = request.data.get("questions")
            count = 1
            for question in questions:
                question_model = Question.objects.get(id=question)
                question_model.order = count
                count = count + 1
                question_model.save()
            return sucess_response(None, 'Question Update Successfully')
        except Question.DoesNotExist:
            return not_found_error("Question Not Found")
