from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_multi_format_email(template_prefix, template_context, target_email):
    template_context.update({
        'base_url': settings.FRONTEND_URL
    })
    subject_file = f'account/{template_prefix}_subject.txt'
    html_file = f'account/{template_prefix}.html'

    from_email = settings.EMAIL_FROM
    bcc_email = settings.EMAIL_BCC
    subject = render_to_string(subject_file).strip()
    html_content = render_to_string(html_file, template_context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [target_email],
        bcc=[bcc_email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
