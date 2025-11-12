import customtkinter as ctk

class ControlPanel:
    def __init__(self, root):
        # O 'root' aqui é, na verdade, a 'right_sidebar_frame'
        # que a View criou. Este é só um "inquilino".
        
        # 1. O Frame principal
        # A gente deixa ele transparente pra ele fingir
        # que é a própria sidebar. Disfarce 10/10.
        self.frame = ctk.CTkFrame(root, fg_color="transparent")
        
        # 2. O Título "Histórico de Ações"
        # Um label bonitinho pra dizer o que é essa caixa.
        self.label = ctk.CTkLabel(self.frame, 
                                  text="Histórico de Ações", 
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  text_color=("#E0E0E0", "#E0E0E0")) # Cor forçada, senão fica apagado
        self.label.pack(pady=(5, 2), padx=10, fill="x")

        # 3. A caixa de texto onde a fofoca rola
        # O CTkTextbox já vem com barra de rolagem. Prático.
        self.log_area = ctk.CTkTextbox(self.frame)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # 4. Trava a caixa (Modo "Só Olhe, Não Toque")
        # Impede o usuário de digitar no log.
        self.log_area.configure(state="disabled")

    # add_log: A única coisa que esse painel sabe fazer.
    # O Controller chama isso pra largar uma fofoca nova.
    def add_log(self, text):
        # "Licença, vou escrever rapidinho..."
        self.log_area.configure(state="normal")
        
        # Escreve a fofoca (o 'text') no final do arquivo
        self.log_area.insert("end", f"> {text}\n")
        
        # Rola pra baixo automaticamente pra mostrar a última fofoca
        self.log_area.see("end")
        
        # "Pronto, pode travar de novo."
        self.log_area.configure(state="disabled")