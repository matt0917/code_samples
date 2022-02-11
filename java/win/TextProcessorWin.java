package win;

import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JLabel;
import javax.swing.JTextPane;
import javax.swing.BoxLayout;

import javax.swing.JButton;
import javax.swing.SpringLayout;
import java.awt.Font;
import java.awt.Color;
import java.awt.ComponentOrientation;
import javax.swing.border.LineBorder;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.HashMap;
import java.util.Set;

import javax.swing.ImageIcon;
import java.awt.Toolkit;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class TextProcessorWin {

	private JFrame main_frame;
	private JTextPane input_textPane;
	private JTextPane stat_textPane;
	private JScrollPane input_scrollPane;
	private JScrollPane stat_scrollPane;
	
	private TextProcessor textProc;
	private String currentText;
	
	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					TextProcessorWin window = new TextProcessorWin();
					window.main_frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public TextProcessorWin() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		main_frame = new JFrame();
		main_frame.setResizable(false);
		main_frame.setIconImage(Toolkit.getDefaultToolkit().getImage(TextProcessorWin.class.getResource("/icon/cookie_monster_icon.png")));
		main_frame.setTitle("Text Processor V1.0");
		main_frame.setBounds(100, 100, 680, 309);
		main_frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		main_frame.getContentPane().setLayout(new BoxLayout(main_frame.getContentPane(), BoxLayout.X_AXIS));
		
		JPanel main_panel = new JPanel();
		main_panel.setBackground(new Color(135, 206, 250));
		main_panel.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
		main_panel.setAutoscrolls(true);
		main_panel.setFont(new Font("Tahoma", Font.PLAIN, 14));
		main_frame.getContentPane().add(main_panel);
		SpringLayout sl_main_panel = new SpringLayout();
		main_panel.setLayout(sl_main_panel);
		
		JPanel panel = new JPanel();
		panel.setBackground(main_panel.getBackground());
		sl_main_panel.putConstraint(SpringLayout.NORTH, panel, 10, SpringLayout.NORTH, main_panel);
		sl_main_panel.putConstraint(SpringLayout.WEST, panel, 10, SpringLayout.WEST, main_panel);
		sl_main_panel.putConstraint(SpringLayout.SOUTH, panel, -10, SpringLayout.SOUTH, main_panel);
		sl_main_panel.putConstraint(SpringLayout.EAST, panel, 388, SpringLayout.WEST, main_panel);
		main_panel.add(panel);
		
		JPanel panel_1 = new JPanel();
		sl_main_panel.putConstraint(SpringLayout.WEST, panel_1, 41, SpringLayout.EAST, panel);
		panel_1.setBackground(main_panel.getBackground());
		sl_main_panel.putConstraint(SpringLayout.NORTH, panel_1, 10, SpringLayout.NORTH, main_panel);
		sl_main_panel.putConstraint(SpringLayout.SOUTH, panel_1, 0, SpringLayout.SOUTH, panel);
		SpringLayout sl_panel = new SpringLayout();
		panel.setLayout(sl_panel);
		
		JLabel input_label = new JLabel("Enter Text:");
		sl_panel.putConstraint(SpringLayout.NORTH, input_label, 0, SpringLayout.NORTH, panel);
		sl_panel.putConstraint(SpringLayout.WEST, input_label, 0, SpringLayout.WEST, panel);
		input_label.setFont(new Font("Tempus Sans ITC", Font.BOLD, 34));
		panel.add(input_label);
		
		input_textPane = new JTextPane();
		input_textPane.addKeyListener(new KeyAdapter() {
			@Override
			public void keyPressed(KeyEvent e) {
				buildLetterMap();
				updateStats();
			}
		});
		input_textPane.setFont(new Font("Tahoma", Font.PLAIN, 14));
		input_scrollPane = new JScrollPane(input_textPane, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
		panel.add(input_scrollPane);
		input_scrollPane.setBorder(new LineBorder(new Color(0, 0, 139), 2, true));
		sl_panel.putConstraint(SpringLayout.NORTH, input_scrollPane, 6, SpringLayout.SOUTH, input_label);
		sl_panel.putConstraint(SpringLayout.WEST, input_scrollPane, 0, SpringLayout.WEST, panel);
		sl_panel.putConstraint(SpringLayout.SOUTH, input_scrollPane, 158, SpringLayout.SOUTH, input_label);
		sl_panel.putConstraint(SpringLayout.EAST, input_scrollPane, 378, SpringLayout.WEST, panel);
		
		JButton clear_btn = new JButton("Clear Text");
		clear_btn.setToolTipText("Press to clear the input text");
		clear_btn.setIcon(new ImageIcon(TextProcessorWin.class.getResource("/icon/cookie_monster_icon.png")));
		clear_btn.addMouseListener(new MouseAdapter() {
			@Override
			public void mousePressed(MouseEvent e) {
				input_textPane.setText("");
				stat_textPane.setText("");
			}
		});
		clear_btn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		clear_btn.setBackground(new Color(255, 215, 0));
		clear_btn.setForeground(new Color(0, 0, 0));
		clear_btn.setFont(new Font("Tempus Sans ITC", Font.BOLD, 24));
		sl_panel.putConstraint(SpringLayout.NORTH, clear_btn, 11, SpringLayout.SOUTH, input_scrollPane);
		sl_panel.putConstraint(SpringLayout.WEST, clear_btn, 0, SpringLayout.WEST, input_label);
		sl_panel.putConstraint(SpringLayout.SOUTH, clear_btn, 50, SpringLayout.SOUTH, input_scrollPane);
		sl_panel.putConstraint(SpringLayout.EAST, clear_btn, 0, SpringLayout.EAST, input_scrollPane);
		panel.add(clear_btn);
		sl_main_panel.putConstraint(SpringLayout.EAST, panel_1, -10, SpringLayout.EAST, main_panel);
		main_panel.add(panel_1);
		SpringLayout sl_panel_1 = new SpringLayout();
		panel_1.setLayout(sl_panel_1);
		
		JLabel stat_label = new JLabel("Stat:");
		sl_panel_1.putConstraint(SpringLayout.NORTH, stat_label, 0, SpringLayout.NORTH, panel_1);
		sl_panel_1.putConstraint(SpringLayout.WEST, stat_label, 0, SpringLayout.WEST, panel_1);
		stat_label.setFont(new Font("Tempus Sans ITC", Font.BOLD, 34));
		panel_1.add(stat_label);
		
		stat_textPane = new JTextPane();
		stat_textPane.setEditable(false);
		stat_textPane.setFont(new Font("Tahoma", Font.PLAIN, 14));
		stat_scrollPane = new JScrollPane(stat_textPane, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
		sl_panel_1.putConstraint(SpringLayout.NORTH, stat_scrollPane, 7, SpringLayout.SOUTH, stat_label);
		sl_panel_1.putConstraint(SpringLayout.WEST, stat_scrollPane, 0, SpringLayout.WEST, panel_1);
		sl_panel_1.putConstraint(SpringLayout.SOUTH, stat_scrollPane, 161, SpringLayout.SOUTH, stat_label);
		sl_panel_1.putConstraint(SpringLayout.EAST, stat_scrollPane, 224, SpringLayout.WEST, panel_1);
		stat_scrollPane.setBorder(new LineBorder(new Color(0, 0, 139), 2, true));
		panel_1.add(stat_scrollPane);	}
	
	
	private void buildLetterMap() {
		currentText = input_textPane.getText().replace("\\s", "");
		textProc = new TextProcessor();
		textProc.buildLetterMap(currentText);
	}
	
	
	private void updateStats() {
		HashMap<Character, Integer> letterMap = textProc.getLetterMap();
		Set<Character> keySet = letterMap.keySet();
		int i = 0;
		String line = String.format("# Total Letter count: %d", currentText.length());
		line = line + "\n" + String.format("# Visible Letter count: %d", keySet.size());
		for (Character l : keySet) {
			++i;
			line = line + "\n" + String.format("%d. %c : %d", i, l, letterMap.get(l));
			stat_textPane.setText(line);
		}
	}
}
