"""
CustomTkinter GUI for the App Store Review Scraper.
Provides a clean interface for fetching and viewing app information and reviews.
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
from datetime import datetime
from typing import Optional, Dict, Any
from app import engine as playstore_engine
from app import appstore_engine
from app.engine import validate_app_id
from app.appstore_engine import validate_app_name


class AppScraperGUI:
    """Main GUI application for the App Store Review Scraper."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.window = ctk.CTk()
        self.window.title("App Store Review Scraper")
        self.window.geometry("1000x700")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Store current data for export
        self.current_data: Optional[Any] = None
        self.data_type: Optional[str] = None  # 'app_info' or 'reviews'
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components."""
        # Main container with padding
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🛍️ App Store Review Scraper",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Input section
        self._create_input_section(main_frame)
        
        # Button section
        self._create_button_section(main_frame)
        
        # Output section
        self._create_output_section(main_frame)
    
    def _create_input_section(self, parent):
        """Create the input fields section."""
        input_frame = ctk.CTkFrame(parent)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Platform selection
        platform_frame = ctk.CTkFrame(input_frame)
        platform_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            platform_frame,
            text="Platform:",
            width=120,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.platform_var = ctk.StringVar(value="Google Play")
        self.platform_menu = ctk.CTkSegmentedButton(
            platform_frame,
            variable=self.platform_var,
            values=["Google Play", "App Store"],
            command=self._on_platform_change
        )
        self.platform_menu.pack(side="left", fill="x", expand=True)
        
        # App ID / App Name
        app_id_frame = ctk.CTkFrame(input_frame)
        app_id_frame.pack(fill="x", padx=10, pady=5)
        
        self.app_id_label = ctk.CTkLabel(
            app_id_frame,
            text="App ID:",
            width=120,
            anchor="w"
        )
        self.app_id_label.pack(side="left", padx=(0, 10))
        
        self.app_id_entry = ctk.CTkEntry(
            app_id_frame,
            placeholder_text="e.g., com.instagram.android"
        )
        self.app_id_entry.pack(side="left", fill="x", expand=True)
        
        # Language and Country on same row
        lang_country_frame = ctk.CTkFrame(input_frame)
        lang_country_frame.pack(fill="x", padx=10, pady=5)
        
        # Language
        ctk.CTkLabel(
            lang_country_frame,
            text="Language:",
            width=120,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.lang_entry = ctk.CTkEntry(
            lang_country_frame,
            width=100,
            placeholder_text="en"
        )
        self.lang_entry.insert(0, "en")
        self.lang_entry.pack(side="left", padx=(0, 20))
        
        # Country
        ctk.CTkLabel(
            lang_country_frame,
            text="Country:",
            width=80,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.country_entry = ctk.CTkEntry(
            lang_country_frame,
            width=100,
            placeholder_text="us"
        )
        self.country_entry.insert(0, "us")
        self.country_entry.pack(side="left")
        
        # Review count and sort
        review_frame = ctk.CTkFrame(input_frame)
        review_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            review_frame,
            text="Review Count:",
            width=120,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.count_entry = ctk.CTkEntry(
            review_frame,
            width=100,
            placeholder_text="100"
        )
        self.count_entry.insert(0, "100")
        self.count_entry.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(
            review_frame,
            text="Sort By:",
            width=80,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.sort_var = ctk.StringVar(value="newest")
        self.sort_menu = ctk.CTkOptionMenu(
            review_frame,
            variable=self.sort_var,
            values=["newest", "rating", "helpfulness"],
            width=150
        )
        self.sort_menu.pack(side="left")
        
        # Text-only filter checkbox
        filter_frame = ctk.CTkFrame(input_frame)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            filter_frame,
            text="Filters:",
            width=120,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.text_only_var = ctk.BooleanVar(value=False)
        self.text_only_checkbox = ctk.CTkCheckBox(
            filter_frame,
            text="Only reviews with text/description",
            variable=self.text_only_var
        )
        self.text_only_checkbox.pack(side="left")
        
        # Output format selection
        output_frame = ctk.CTkFrame(input_frame)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            output_frame,
            text="Output Format:",
            width=120,
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        self.output_format_var = ctk.StringVar(value="Full")
        self.output_format_menu = ctk.CTkOptionMenu(
            output_frame,
            variable=self.output_format_var,
            values=["Full", "Text only", "Title + Text"],
            width=150
        )
        self.output_format_menu.pack(side="left")
    
    def _create_button_section(self, parent):
        """Create the action buttons section."""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # First row of buttons
        row1 = ctk.CTkFrame(button_frame)
        row1.pack(fill="x", pady=(0, 5))
        
        self.app_info_btn = ctk.CTkButton(
            row1,
            text="📱 Crawl App Info",
            command=self._crawl_app_info,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.app_info_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.reviews_btn = ctk.CTkButton(
            row1,
            text="⭐ Crawl Reviews",
            command=self._crawl_reviews,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.reviews_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.multi_country_btn = ctk.CTkButton(
            row1,
            text="🌍 Multi-Country Reviews",
            command=self._crawl_reviews_multi_country,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="purple",
            hover_color="darkviolet"
        )
        self.multi_country_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # Second row of buttons
        row2 = ctk.CTkFrame(button_frame)
        row2.pack(fill="x")
        
        self.export_btn = ctk.CTkButton(
            row2,
            text="💾 Export JSON",
            command=self._export_json,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.export_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.clear_btn = ctk.CTkButton(
            row2,
            text="🗑️ Clear",
            command=self._clear_output,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.clear_btn.pack(side="left", padx=5, expand=True, fill="x")
    
    def _on_platform_change(self, value):
        """Handle platform selection change."""
        if value == "Google Play":
            self.app_id_label.configure(text="App ID:")
            self.app_id_entry.configure(placeholder_text="e.g., com.instagram.android")
            self.lang_entry.configure(state="normal")
        else:  # App Store
            self.app_id_label.configure(text="App Name or ID:")
            self.app_id_entry.configure(placeholder_text="e.g., instagram or 389801252")
            self.lang_entry.delete(0, "end")
            self.lang_entry.insert(0, "N/A")
            self.lang_entry.configure(state="disabled")
    
    def _create_output_section(self, parent):
        """Create the output display section."""
        output_frame = ctk.CTkFrame(parent)
        output_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Label
        ctk.CTkLabel(
            output_frame,
            text="Results:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10, 5))
        
        # Status message label (for success/error messages)
        self.status_label = ctk.CTkLabel(
            output_frame,
            text="",
            font=ctk.CTkFont(size=12),
            anchor="w",
            wraplength=950
        )
        self.status_label.pack(fill="x", padx=10, pady=(0, 5))
        
        # Text box with scrollbar
        self.output_text = ctk.CTkTextbox(
            output_frame,
            font=ctk.CTkFont(family="Monaco", size=12),
            wrap="word"
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def _get_input_values(self) -> Dict[str, Any]:
        """Get and validate input values from the form."""
        app_id = self.app_id_entry.get().strip()
        lang = self.lang_entry.get().strip() or "en"
        country = self.country_entry.get().strip() or "us"
        
        try:
            count = int(self.count_entry.get().strip() or "100")
            if count <= 0:
                raise ValueError("Count must be positive")
        except ValueError:
            count = 100
        
        sort_by = self.sort_var.get()
        platform = self.platform_var.get()
        text_only = self.text_only_var.get()
        
        return {
            "app_id": app_id,
            "lang": lang,
            "country": country,
            "count": count,
            "sort": sort_by,
            "platform": platform,
            "text_only": text_only
        }
    
    def _validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate input values."""
        platform = inputs.get("platform", "Google Play")
        
        if not inputs["app_id"]:
            field_name = "App Name or ID" if platform == "App Store" else "App ID"
            messagebox.showerror("Error", f"Please enter an {field_name}")
            return False
        
        # Validate based on platform
        if platform == "Google Play":
            if not validate_app_id(inputs["app_id"]):
                messagebox.showwarning(
                    "Warning",
                    "App ID format may be invalid. Expected format: com.company.app"
                )
        else:  # App Store
            # For App Store, accept either numeric ID or app name
            # Numeric IDs are preferred and always valid
            if not inputs["app_id"].isdigit():
                # If not numeric, validate as app name
                if not validate_app_name(inputs["app_id"]):
                    messagebox.showwarning(
                        "Warning",
                        "Please enter a valid app name or numeric app ID (recommended)."
                    )
        
        return True
    
    def _crawl_app_info(self):
        """Crawl and display app information."""
        inputs = self._get_input_values()
        
        if not self._validate_inputs(inputs):
            return
        
        # Disable buttons during operation
        self._set_buttons_state("disabled")
        self._update_output("Fetching app information...\n")
        self.window.update()
        
        try:
            # Select the appropriate engine
            platform = inputs.get("platform", "Google Play")
            
            if platform == "Google Play":
                result = playstore_engine.fetch_app_info(
                    app_id=inputs["app_id"],
                    lang=inputs["lang"],
                    country=inputs["country"]
                )
                title_key = "title"
            else:  # App Store
                result = appstore_engine.fetch_app_info(
                    app_name=inputs["app_id"],
                    country=inputs["country"]
                )
                title_key = "app_name"
            
            # Check for errors
            if "error" in result:
                error_msg = result["error"]
                if "suggestion" in result:
                    error_msg += f" {result['suggestion']}"
                self._show_status(f"❌ Error: {error_msg}", "error")
                self._update_output(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                # Store data for export
                self.current_data = result
                self.data_type = "app_info"
                
                # Display formatted JSON
                json_str = json.dumps(result, indent=2, ensure_ascii=False)
                self._update_output(json_str)
                
                title = result.get(title_key, result.get("title", "N/A"))
                self._show_status(f"✅ Successfully fetched info for: {title}", "success")
        
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self._show_status(f"❌ {error_msg}", "error")
            self._update_output(error_msg + "\n")
        
        finally:
            self._set_buttons_state("normal")
    
    def _crawl_reviews(self):
        """Crawl and display app reviews."""
        inputs = self._get_input_values()
        
        if not self._validate_inputs(inputs):
            return
        
        # Disable buttons during operation
        self._set_buttons_state("disabled")
        self._update_output(f"Fetching reviews...\n")
        self.window.update()
        
        try:
            # Select the appropriate engine
            platform = inputs.get("platform", "Google Play")
            
            if platform == "Google Play":
                result = playstore_engine.fetch_app_reviews(
                    app_id=inputs["app_id"],
                    count=inputs["count"],
                    lang=inputs["lang"],
                    country=inputs["country"],
                    sort=inputs["sort"],
                    text_only=inputs["text_only"]
                )
            else:  # App Store
                result = appstore_engine.fetch_app_reviews(
                    app_name=inputs["app_id"],
                    country=inputs["country"],
                    count=inputs["count"],
                    sort="mostRecent" if inputs["sort"] == "newest" else "mostHelpful",
                    text_only=inputs["text_only"]
                )
            
            # Check for errors
            if result and isinstance(result, list) and "error" in result[0]:
                error_msg = result[0]["error"]
                if "suggestion" in result[0]:
                    error_msg += f" {result[0]['suggestion']}"
                self._show_status(f"❌ Error: {error_msg}", "error")
                self._update_output(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                # Store data for export
                self.current_data = result
                self.data_type = "reviews"
                
                # Apply output formatting
                output_format = self.output_format_var.get()
                formatted_result = self._format_output(result, output_format)
                
                # Display formatted JSON
                json_str = json.dumps(formatted_result, indent=2, ensure_ascii=False)
                self._update_output(json_str)
                
                # Create informative message
                actual_count = len(result)
                requested_count = inputs["count"]
                text_only_note = " (text only)" if inputs["text_only"] else ""
                
                message = f"✅ Successfully fetched {actual_count} reviews{text_only_note}"
                if actual_count < requested_count:
                    message += f" (requested {requested_count}). Try multi-country for more reviews."
                
                self._show_status(message, "success")
        
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self._show_status(f"❌ {error_msg}", "error")
            self._update_output(error_msg + "\n")
        
        finally:
            self._set_buttons_state("normal")
    
    def _crawl_reviews_multi_country(self):
        """Crawl reviews from multiple countries to get more comprehensive data."""
        inputs = self._get_input_values()
        
        if not self._validate_inputs(inputs):
            return
        
        # Disable buttons during operation
        self._set_buttons_state("disabled")
        self._update_output("Fetching reviews from multiple countries...\nThis may take a while...\n")
        self.window.update()
        
        try:
            # Select the appropriate engine
            platform = inputs.get("platform", "Google Play")
            
            if platform == "Google Play":
                result = playstore_engine.fetch_reviews_multi_country(
                    app_id=inputs["app_id"],
                    count_per_country=inputs["count"],
                    lang=inputs["lang"],
                    sort=inputs["sort"],
                    text_only=inputs["text_only"]
                )
            else:  # App Store
                result = appstore_engine.fetch_reviews_multi_country(
                    app_name=inputs["app_id"],
                    count_per_country=inputs["count"],
                    sort="mostRecent" if inputs["sort"] == "newest" else "mostHelpful",
                    text_only=inputs["text_only"]
                )
            
            # Check if we got results
            if not result or (isinstance(result, list) and "error" in result[0]):
                error = result[0]["error"] if result else "No reviews found"
                self._show_status(f"❌ Error: {error}", "error")
                self._update_output(f"Error: {error}\n")
            else:
                # Store data for export
                self.current_data = result
                self.data_type = "reviews_multi_country"
                
                # Apply output formatting
                output_format = self.output_format_var.get()
                formatted_result = self._format_output(result, output_format)
                
                # Display formatted JSON
                json_str = json.dumps(formatted_result, indent=2, ensure_ascii=False)
                self._update_output(json_str)
                
                text_only_note = " (text only)" if inputs["text_only"] else ""
                # Show success message
                self._show_status(
                    f"✅ Successfully fetched {len(result)} unique reviews{text_only_note} from multiple countries! "
                    f"Each review has a 'fetched_from_country' field.",
                    "success"
                )
        
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self._show_status(f"❌ {error_msg}", "error")
            self._update_output(error_msg + "\n")
        
        finally:
            self._set_buttons_state("normal")
    
    def _export_json(self):
        """Export current data to JSON file."""
        if not self.current_data:
            self._show_status("⚠️ No data to export", "warning")
            return
        
        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{self.data_type}_{timestamp}.json"
        
        # Open file dialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=default_filename,
            initialdir="./data"
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.current_data, f, indent=2, ensure_ascii=False)
            
            self._show_status(f"✅ Data exported successfully to: {filepath}", "success")
        
        except Exception as e:
            self._show_status(f"❌ Failed to export data: {str(e)}", "error")
    
    def _clear_output(self):
        """Clear the output display."""
        self._update_output("")
        self._show_status("", "normal")
        self.current_data = None
        self.data_type = None
    
    def _update_output(self, text: str):
        """Update the output text box."""
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
    
    def _format_output(self, data: Any, output_format: str) -> Any:
        """Format the output data based on selected format.
        
        Args:
            data: The data to format (can be list of reviews or app info)
            output_format: "Full", "Text only", or "Title + Text"
        
        Returns:
            Formatted data
        """
        # If it's app info or error, return as-is
        if isinstance(data, dict):
            return data
        
        # If it's not a list of reviews, return as-is
        if not isinstance(data, list) or not data:
            return data
        
        # Check if first item is an error
        if "error" in data[0]:
            return data
        
        # Apply formatting based on selection
        if output_format == "Text only":
            return [{"text": review.get("text", "")} for review in data]
        elif output_format == "Title + Text":
            return [
                {
                    "title": review.get("title", ""),
                    "text": review.get("text", "")
                }
                for review in data
            ]
        else:  # Full
            return data
    
    def _show_status(self, message: str, status_type: str = "normal"):
        """Show status message above results.
        
        Args:
            message: The message to display
            status_type: 'success', 'error', 'warning', or 'normal'
        """
        self.status_label.configure(text=message)
        
        # Set color based on status type
        if status_type == "success":
            self.status_label.configure(text_color="#4ade80")  # green
        elif status_type == "error":
            self.status_label.configure(text_color="#f87171")  # red
        elif status_type == "warning":
            self.status_label.configure(text_color="#fbbf24")  # yellow
        else:
            self.status_label.configure(text_color="#9ca3af")  # gray
    
    def _set_buttons_state(self, state: str):
        """Enable or disable all buttons."""
        buttons = [
            self.app_info_btn,
            self.reviews_btn,
            self.multi_country_btn,
            self.export_btn,
            self.clear_btn
        ]
        
        for btn in buttons:
            btn.configure(state=state)
    
    def run(self):
        """Start the GUI application."""
        self.window.mainloop()


def main():
    """Main entry point for the GUI."""
    app = AppScraperGUI()
    app.run()


if __name__ == "__main__":
    main()
