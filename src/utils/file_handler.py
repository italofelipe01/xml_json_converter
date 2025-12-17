"""
Módulo para manipulação de arquivos
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any


class FileHandler:
    """
    Classe para operações com arquivos
    """

    def __init__(self):
        """Inicializa o manipulador de arquivos"""
        self.supported_encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    def validate_file_exists(self, file_path: Union[str, Path]) -> bool:
        """
        Valida se arquivo existe

        Args:
            file_path: Caminho do arquivo

        Returns:
            True se arquivo existe
        """
        return Path(file_path).exists()

    def validate_is_file(self, file_path: Union[str, Path]) -> bool:
        """
        Valida se é um arquivo (não diretório)

        Args:
            file_path: Caminho do arquivo

        Returns:
            True se é arquivo
        """
        path = Path(file_path)
        return path.exists() and path.is_file()

    def get_file_extension(self, file_path: Union[str, Path]) -> str:
        """
        Obtém extensão do arquivo

        Args:
            file_path: Caminho do arquivo

        Returns:
            Extensão do arquivo (sem o ponto)
        """
        return Path(file_path).suffix.lower().lstrip(".")

    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """
        Obtém tamanho do arquivo em bytes

        Args:
            file_path: Caminho do arquivo

        Returns:
            Tamanho em bytes
        """
        try:
            return Path(file_path).stat().st_size
        except (OSError, FileNotFoundError):
            return 0

    def get_file_info(self, file_path: Union[str, Path]) -> Dict:
        """
        Obtém informações completas do arquivo

        Args:
            file_path: Caminho do arquivo

        Returns:
            Dict com informações do arquivo
        """
        path = Path(file_path)

        if not path.exists():
            return {"exists": False}

        try:
            stat = path.stat()
            return {
                "exists": True,
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
                "name": path.name,
                "stem": path.stem,
                "suffix": path.suffix,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified": stat.st_mtime,
                "created": stat.st_ctime,
                "absolute_path": str(path.absolute()),
            }
        except OSError as e:
            return {"exists": True, "error": str(e)}

    def read_file(
        self, file_path: Union[str, Path], encoding: Optional[str] = None
    ) -> Optional[str]:
        """
        Lê conteúdo de arquivo texto

        Args:
            file_path: Caminho do arquivo
            encoding: Encoding específico (tenta automático se None)

        Returns:
            Conteúdo do arquivo ou None em caso de erro
        """
        path = Path(file_path)

        if not self.validate_is_file(path):
            print(f"❌ Arquivo não encontrado ou não é um arquivo: {path}")
            return None

        # Lista de encodings para tentar
        encodings_to_try = [encoding] if encoding else self.supported_encodings

        for enc in encodings_to_try:
            try:
                with open(path, "r", encoding=enc) as file:
                    content = file.read()
                    if content.strip():  # Verifica se não está vazio
                        return content
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                print(f"❌ Erro ao ler arquivo {path}: {e}")
                return None

        print(
            f"❌ Não foi possível ler o arquivo com nenhum encoding suportado: {path}"
        )
        return None

    def write_file(
        self,
        content: str,
        file_path: Union[str, Path],
        encoding: str = "utf-8",
        create_dirs: bool = True,
    ) -> bool:
        """
        Escreve conteúdo em arquivo

        Args:
            content: Conteúdo a ser escrito
            file_path: Caminho do arquivo
            encoding: Encoding do arquivo
            create_dirs: Se deve criar diretórios pai

        Returns:
            True se escreveu com sucesso
        """
        try:
            path = Path(file_path)

            # Cria diretórios se necessário
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding=encoding) as file:
                file.write(content)

            return True

        except Exception as e:
            print(f"❌ Erro ao escrever arquivo {file_path}: {e}")
            return False

    def write_json_file(
        self,
        data: Any,
        file_path: Union[str, Path],
        create_dirs: bool = True,
        **json_kwargs,
    ) -> bool:
        """
        Escreve dados em arquivo JSON

        Args:
            data: Dados para salvar
            file_path: Caminho do arquivo
            create_dirs: Se deve criar diretórios pai
            **json_kwargs: Argumentos para json.dump

        Returns:
            True se salvou com sucesso
        """
        try:
            path = Path(file_path)

            # Cria diretórios se necessário
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)

            # Configurações padrão para JSON
            default_json_kwargs = {
                "indent": 2,
                "ensure_ascii": False,
                "separators": (",", ": "),
            }
            default_json_kwargs.update(json_kwargs)

            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, **default_json_kwargs)

            return True

        except Exception as e:
            print(f"❌ Erro ao salvar JSON {file_path}: {e}")
            return False

    def list_files(
        self, directory: Union[str, Path], pattern: str = "*", recursive: bool = False
    ) -> List[Path]:
        """
        Lista arquivos em diretório

        Args:
            directory: Diretório para listar
            pattern: Padrão de arquivos (glob)
            recursive: Se deve buscar recursivamente

        Returns:
            Lista de caminhos de arquivos
        """
        try:
            dir_path = Path(directory)

            if not dir_path.exists() or not dir_path.is_dir():
                print(f"❌ Diretório não encontrado: {directory}")
                return []

            if recursive:
                files = list(dir_path.rglob(pattern))
            else:
                files = list(dir_path.glob(pattern))

            # Filtra apenas arquivos (não diretórios)
            return [f for f in files if f.is_file()]

        except Exception as e:
            print(f"❌ Erro ao listar arquivos: {e}")
            return []

    def create_directory(self, dir_path: Union[str, Path]) -> bool:
        """
        Cria diretório

        Args:
            dir_path: Caminho do diretório

        Returns:
            True se criou com sucesso
        """
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"❌ Erro ao criar diretório {dir_path}: {e}")
            return False

    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """
        Remove arquivo

        Args:
            file_path: Caminho do arquivo

        Returns:
            True se removeu com sucesso
        """
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                return True
            else:
                print(f"❌ Arquivo não encontrado: {file_path}")
                return False
        except Exception as e:
            print(f"❌ Erro ao remover arquivo {file_path}: {e}")
            return False

    def get_available_space(self, path: Union[str, Path]) -> Dict:
        """
        Obtém espaço disponível no sistema de arquivos

        Args:
            path: Caminho para verificar espaço

        Returns:
            Dict com informações de espaço
        """
        try:
            stat = os.statvfs(str(path))

            # Calcula espaços em bytes
            total = stat.f_frsize * stat.f_blocks
            available = stat.f_frsize * stat.f_bavail
            used = total - available

            return {
                "total_bytes": total,
                "available_bytes": available,
                "used_bytes": used,
                "total_gb": round(total / (1024**3), 2),
                "available_gb": round(available / (1024**3), 2),
                "used_gb": round(used / (1024**3), 2),
                "usage_percent": round((used / total) * 100, 1) if total > 0 else 0,
            }
        except (AttributeError, OSError):
            # statvfs não disponível no Windows, usa alternativa
            try:
                import shutil

                total, used, free = shutil.disk_usage(str(path))
                return {
                    "total_bytes": total,
                    "available_bytes": free,
                    "used_bytes": used,
                    "total_gb": round(total / (1024**3), 2),
                    "available_gb": round(free / (1024**3), 2),
                    "used_gb": round(used / (1024**3), 2),
                    "usage_percent": round((used / total) * 100, 1) if total > 0 else 0,
                }
            except Exception as e:
                print(f"❌ Erro ao obter informações de espaço: {e}")
                return {}

    def backup_file(
        self, file_path: Union[str, Path], backup_suffix: str = ".bak"
    ) -> bool:
        """
        Cria backup de arquivo

        Args:
            file_path: Caminho do arquivo original
            backup_suffix: Sufixo do arquivo de backup

        Returns:
            True se criou backup com sucesso
        """
        try:
            path = Path(file_path)

            if not path.exists():
                print(f"❌ Arquivo não encontrado para backup: {file_path}")
                return False

            backup_path = path.with_suffix(path.suffix + backup_suffix)

            # Copia conteúdo
            import shutil

            shutil.copy2(path, backup_path)

            print(f"📋 Backup criado: {backup_path}")
            return True

        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
