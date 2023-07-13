from fpdf import FPDF, HTMLMixin

class PDF(FPDF, HTMLMixin):
    def title(self, title):
        self.set_font("helvetica", "B", 24)
        self.cell(w=0, txt=title, align="C")
        self.ln(12)
    
    def para_title(self, num, title, url):
        self.set_font("helvetica", "B", 16)
        self.set_text_color(10,101,34)
        self.cell(w=210, txt=(str(num) + ". " + title), link=url)
        self.ln(8)
        
    def para_subtitle(self, subtitle):
        self.set_font("helvetica", "I", 12)
        self.set_text_color(0,0,0)
        self.cell(w=210, txt=subtitle)
        self.ln(8)
    
    def para_subtitle_bold(self, subtitle_bold):
        self.set_font("helvetica", "B", 12)
        self.set_text_color(0,0,0)
        self.cell(w=210, txt=subtitle_bold)
        self.ln(8)
    
    def para_body(self, body):
        self.set_font("helvetica", "", 12)
        self.set_text_color(0,0,0)
        self.write_html(text=body)
        self.ln(12)
    
    def print_para(self, num, title, link, subtitle, subtitle_bold, body):
        self.para_title(num, title, link)
        self.para_subtitle(subtitle)
        self.para_subtitle_bold(subtitle_bold)
        self.para_body(body)